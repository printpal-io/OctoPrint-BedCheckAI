from __future__ import absolute_import
import octoprint.plugin
from uuid import uuid4
from .utils import *
from base64 import b64encode
CONST_MAX_QUERIES_NOLOGIN = 20

class BedCheckAIPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.SimpleApiPlugin
    ):

    def on_after_startup():
        if self._settings.get(["printer_id"]) == '':
            self._settings.set(["printer_id"], uuid4().hex)
            self._settings.save(force=True, trigger_event=False)
        self.get_baseline()
        self._logger.info('PRINT BED AI STARTUP: {}'.format(self._settings.get([])))
        self._logger.info('pid: {}'.format(self._settings.get(["printer_id"])))

    def get_api_commands(self):
        return dict(
            update_baseline=[],
            analyze=[],
            get_baseline=[],
        )

    def get_settings_defaults(self):
        return {
            "snapshot_url" : "http://localhost/webcam/?action=snapshot",
            "api_key" : '',
            "printer_id" : '',
            "cancel_print" : False,
            "pause_print" : False,
            "queries" : 0,
            "current_uid" : '',
            "threshold" : 50
        }

    def get_template_configs(self) -> list:
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return {
            "js": ["js/bedcheckai.js"],
            "css" : ["css/bedcheckai.css"]
        }

    def segment_snap(self, compare : bool = False):
        status_, r_img_, loss_, uid_ = None, None, None, None
        snap_addr_ = self._settings.get(["snapshot_url"])
        if len(snap_addr_) < 5 or not snap_addr_.startswith("http"):
            self._logger.info("Webcam snapshot url incorrect: {}".format(snap_addr_))
        byte_image_ = snap_sync(snap_addr_)
        if byte_image_ is False:
            self._logger.info("Grabbing snapshot frame failed")
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="camera", result="fail"))
        else:
            seg_ = send_infer(byte_image_, self._settings, compare)
            self._logger.info("Bed Segment response: {}".format(seg_))
            if seg_ is not None:
                status_ = seg_.get("status")
                if status_ == 8000:
                    items_ = seg_.get('items', {}).get("status", {})
                    r_img_, loss_, uid_ = items_.get("mask"), items_.get("loss"), items_.get("unique_id")
            self._settings.set(['queries'], self._settings.get(['queries']) + 1)
            self._settings.save(force=True, trigger_event=False)

        return status_, r_img_, loss_, uid_

    def update_baseline(self, uid_ : str):
        response_ = update_baseline_(self._settings, uid_)
        self._logger.info("UPDATE BASELINE RESPONSE: {}".format(response_))

        if response_ is None:
            # Something went wrong with updating the baseline
            # See plugin log for more
            # Throw fail message to UI
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="baseline", result="fail"))
        else:
            # Throw success message to UI
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="baseline", result="success"))
        return response_

    def get_baseline(self):
        r_ = get_baseline_(self._settings)
        if r_ is None or r_.get("status") != 8000:
            # Issue
            info_ = str(r_) if r_ is not None else 'None'
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="baseline_get", result="fail", info=info_))
        else:
            mask_ = 'data:image/png;charset=utf-8;base64,' + r_.get("items", {}).get("status", {}).get("mask").split('\n')[0]
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="baseline_get", result="success", mask=mask_))

    def analyze(self, compare : bool = False):
        if self._settings.get(["queries"]) < CONST_MAX_QUERIES_NOLOGIN or self._settings.get(["api_key"]) not in [None, '']:
            if self._settings.get(["printer_id"]) in [None, '']:
                self._settings.set(["printer_id"], uuid4().hex)
            status, img, loss, uid = self.segment_snap(compare)
            img = 'data:image/png;charset=utf-8;base64,' + img.split('\n')[0]
            self._settings.set(["current_uid"], uid)
            self._settings.save(force=True, trigger_event=False)
            return {"status" : status , "mask_preview" : img, "loss" : loss, "threshold" : self._settings.get_int(["threshold"]) / 1000}
        else:
            self._plugin_manager.send_plugin_message(self._identifier, dict(type="queries", result="maxed"))
            self._logger.info("MAX queries OR bad api key")
            return {"status" : 8005}

    def on_api_command(self, command, data):
        import flask
        if command == "analyze":
            try:
                r_ = self.analyze(compare=data.get("compare"))
                return flask.jsonify(r_)
            except Exception as e:
                return flask.jsonify({"status" : 8006, "response" : str(e)})
        elif command == "update_baseline":
            try:
                r_ = self.update_baseline(self._settings.get(["current_uid"]))
                return flask.jsonify(r_)
            except Exception as e:
                return flask.jsonify({'e' : str(e)})
        elif command == "get_baseline":
            try:
                self.get_baseline()
                return flask.jsonify({})
            except Exception as e:
                return flask.jsonify({'e' : str(e)})

    def process_at_command(self, comm, phase, command, parameters, tags=None, *args, **kwargs):
        if command.upper() != "SEGMENTBED":
            return

        with self._printer.job_on_hold():
            try:
                r_ = self.analyze(compare=True)
                self._logger.info("Segment analysis: {}".format(r_))
                if r_.get("loss") >= (self._settings.get_int(["threshold"]) / 1000):
                    if self._settings.get(["cancel_print"]):
                        self._printer.cancel_print(tags={self._identifier})
                    elif self._settings.get(["pause_print"]):
                        self._printer.pause_print(tags={self._identifier})
                r_["type"] = 'atcommand'
                self._plugin_manager.send_plugin_message(self._identifier, r_)
            except Exception as e:
                self._logger.info('Error processing @ command: {}'.format(str(e)))

    def get_update_information(self):
        return {
            "bedready": {
                "displayName": "Bed Check AI",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "printpal-io",
                "repo": "OctoPrint-BedCheckAI",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/printpal-io/OctoPrint-BedCheckAI/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Bed Check AI"
__plugin_pythoncompat__ = ">=3.6,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = BedCheckAIPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.atcommand.queuing": __plugin_implementation__.process_at_command
    }

    global __plugin_helpers__
    __plugin_helpers__ = {
            'analyze': __plugin_implementation__.analyze,
            'set_baseline': __plugin_implementation__.update_baseline,
            }

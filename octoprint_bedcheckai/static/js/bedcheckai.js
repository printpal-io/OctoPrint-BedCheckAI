$(function() {
    function BedcheckaiViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];
        self.currentPreview = ko.observable(null);
        self.currentBaseline = ko.observable(null);
        self.analyzing = ko.observable(false);
        self.currentLoss = ko.observable(0.0);
        self.bedStatus = ko.observable(null);
        self.bedStatusColor = ko.observable("green");

        self.onStartupComplete = function() {
          if (self.currentBaseline() == null) {
            self.get_baseline()
          }
            // render baseline image and settings
        }

        self.onDataUpdaterPluginMessage = function(plugin, data){
          if (plugin=="bedcheckai" && data.type=="atcommand"){
            self.currentPreview(data.image);
            if (data.status == 8000) {
              let result_title = '';
              if (data.loss <= data.threshold) {
                result_title = 'BED CLEAR';
              } else {
                result_title = 'BED NOT CLEAR';
              }
              new PNotify({
                  title: result_title,
                  text: 'Loss: ' + data.loss ,
                  hide: true
              });
            } else {
              new PNotify({
                  title: 'Error Analyzing Bed',
                  text: 'Status: ' + data.status,
                  hide: true
              });
            }
          } else if (plugin=="bedcheckai" && data.type=="baseline") {
            console.log('Got plugin message: ' + data);
            new PNotify({
                title: 'Baseline Update',
                text: 'Result: ' + data.result,
                hide: true
            });
            if (data.result == 'success') {
              console.log('Got plugin message success for baseline');
              self.currentBaseline(self.currentPreview());
            }
          } else if (plugin=="bedcheckai" && data.type=="queries") {
            new PNotify({
                title: 'Max Bed Detections Reached',
                text: 'Please register a free account on https://app.printpal.io to continue using the bed check AI feature (its still free, just verify your account).',
                hide: true
            });
          } else if (plugin=="bedcheckai" && data.type=="camera") {
            new PNotify({
                title: 'Error retrieveing snapshot',
                text: 'Check snapshot URL setting in Bed Check AI plugin.',
                hide: true
            });
          } else if (plugin=="bedcheckai" && data.type=="baseline_get") {
            if (data.result == 'fail') {
              new PNotify({
                  title: 'Error retrieveing baseline',
                  text: 'Set a baseline image.',
                  hide: true
              });
            } else {
              self.currentBaseline(data.mask);
            }
          }
          return ;
        }

        self.analyze_frame = function() {
            self.analyzing(true);
            OctoPrint.simpleApiCommand('bedcheckai', 'analyze', {compare: true})
                .done(function (response) {
                  if (response.status == 8000) {
                    self.currentPreview(response.mask_preview);
                    self.currentLoss(response.loss.toFixed(8));
                    if (response.loss >= response.threshold) {
                      self.bedStatus("NOT CLEAR");
                      self.bedStatusColor("red");
                    } else {
                      self.bedStatus("CLEAR");
                      self.bedStatusColor("green");
                    }

                  }
                  else {
                    new PNotify({
                        title: 'Bed Analysis Fail',
                        text: 'Error: ' + response.status,
                        hide: true
                    });
                  }
                  self.analyzing(false);
                })
                .fail(function (response) {
                  new PNotify({
                      title: 'Bed Check fail',
                      text: 'Error: ' + response.responseJSON.error,
                      hide: true
                  });
                  self.analyzing(false);
                });
        };

        self.update_baseline = function() {
            self.analyzing(true);
            OctoPrint.simpleApiCommand('bedcheckai', 'update_baseline')
                .done(function (response) {
                  self.analyzing(false);
                })
                .fail(function (response) {
                  new PNotify({
                      title: 'Bed Check fail',
                      text: 'Error: ' + response.responseJSON.error,
                      hide: true
                  });
                  self.analyzing(false);
                });
        };

        self.get_baseline = function() {
            OctoPrint.simpleApiCommand('bedcheckai', 'get_baseline')
                .done(function (response) {
                })
                .fail(function (response) {
                  new PNotify({
                      title: 'Failed to retrieve baseline',
                      text: 'Error: ' + response.responseJSON.error,
                      hide: true
                  });
                });
        };
    }


    OCTOPRINT_VIEWMODELS.push([
        BedcheckaiViewModel,
        ["settingsViewModel", "controlViewModel"],
        ["#tab_plugin_bedcheckai"]
    ]);
});

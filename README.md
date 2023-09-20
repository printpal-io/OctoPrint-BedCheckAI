<p align="center">
    <br>
    <img src="/extras/images/bed-check-ai.png" width="600"/>
    <br>
<p>
<p align="center">
    <a href="https://printpal.io/">
        <img alt="Documentation" src="https://img.shields.io/badge/website-online-brightgreen">
    </a>
    <a href="https://github.com/printpal-io/OctoPrint-PrintWatch/releases">
        <img alt="GitHub release" src="https://img.shields.io/badge/release-1.0.0-blue">
    </a>
    <a href="https://printpal.pythonanywhere.com/api/status">
        <img alt="API Status" src="https://img.shields.io/badge/API-online-brightgreen">
    </a>
    <a href="https://discord.gg/DRM7w88AbS">
        <img alt="Discord Server" src="https://img.shields.io/badge/discord-online-blueviolet?logo=discord">
    </a>
</p>
<h2 align="center">
  OctoPrint-BedCheckAI
</h2>
<p>
  Bed Check AI uses Artificial Intelligence to detect your 3D printer's bed. The plugin takes the snapshot from any camera compatible with OctoPrint and runs it through a Machine Learning model that detects the entire print bed area. Based on the analysis, we can tell if:
</p>
<ul>
  <li>The print bed is clear of the previous print</li>
  <li>A foreign object is on the bed (clippers, tools, etc.)</li>
  <li>The location and sizes of any objects</li>
</ul>
<h3>
  Setup
</h3>
<p>
    1. Open the <b>OctoPrint Web Inferface</b>
</p>
<p>
    2. Open the <b>Settings</b> using the 🔧 (wrench) icon in the top right header
</p>
<p>
    3. Open the <b>Plugin Manager</b> in the left-side selection menu
</p>
<p>
    4. Click on the <b>"+ Get More"</b> button
</p>
<p>
    5. Search for <b>BedCheckAI</b>
</p>
<p>
    6. Click <b>Install</b> on the PrintWatch Plugin
</p>
<p>
  7. Restart OctoPrint once Installation is completed
</p>
<p>
  The full installation guide/quickstart can be found here: <a href="https://github.com/printpal-io/OctoPrint-BedCheckAI/wiki/Installation">QuickStart Guide with OctoPrint</a>
</p>
<h3>
  Configuration
</h3>
<p>
  Once you have successfully installed BedCheckAI, you should configure the settings. To configure the settings:
</p>
<p>
    1. Open the <b>OctoPrint Web Inferface</b>
</p>
<p>
    2. Open the <b>Settings</b> using the 🔧 (wrench) icon in the top right header
</p>
<p>
    3. Scroll down to the <b>Plugin Settings</b> in the left-side selection menu and select <b>'Bed Check AI'</b>
</p>
<p>
    The Settings for PrintWatch include:
</p>
<table>
  <tr>
    <td>
      <b>Setting</b>
    </td>
    <td>
      <b>Description</b>
    </td>
  </tr>
  <tr>
    <td>
      API Key
    </td>
    <td>
      The secret key used to authenticate API usage. Get yours Free <a href="https://printpal.io/pricing/">here</a>
    </td>
  </tr>
  <tr>
    <td>
      Snapshot URL
    </td>
    <td>
      The webcam snapshot address of your camera
    </td>
  </tr>
  <tr>
    <td>
      Pause Print
    </td>
    <td>
      Toggle whether the print is paused if the bed is detected to be NOT CLEAR.
    </td>
  </tr>
  <tr>
    <td>
      Cancel Print
    </td>
    <td>
      Toggle whether the print is cancelled if the bed is detected to be NOT CLEAR.
    </td>
  </tr>
  <tr>
    <td>
      Threshold
    </td>
    <td>
      The threshold at which the bed is classified as CLEAR vs NOT CLEAR.
    </td>
  </tr>
</table>
<br>

<h3>Our Other Plugins</h3>
<table>
  <tr>
    <td>
      <p align="left">
    <br>
    <a href="https://github.com/printpal-io/OctoPrint-PrintWatch">
      <img src="https://printpal.io/wp-content/uploads/2022/01/printwatch_logo_gh.png" width="400"/>
    </a>
    <br>
    <p>
    <h4>PrintWatch AI monitoring & Remote Access</h4>
    <p>
      This plugin monitors your prints in real-time for defects and failures and notifies you<br> 
      and/or pauses the print so you save time, material, and gain peace of mind. This plugin<br> 
      also allows you to remotely view and manage your printer from anywhere in the world.
    </p>
      <p>
        Check it out on the <a href="https://plugins.octoprint.org/plugins/printwatch/">OctoPrint Plugin Manager</a> or click <a href="https://github.com/printpal-io/OctoPrint-PrintWatch">here</a>
      </p>
      <br>
        <img src="/extras/images/ai-example.gif"/>
      <br>
    </td>
  </tr>
</table>

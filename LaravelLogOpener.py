import sublime
import sublime_plugin
import re, os

class LaravelLogOpenerCommand(sublime_plugin.WindowCommand):


  def run(self):
    if not self.window.active_view(): return

    # What file are we looking for?
    logfile_name = "laravel"
    file_matcher = re.compile(r"[/\\]" + logfile_name + "\.log$")

    # Get current file so we can get the project root from this.
    current_file_path = self.window.active_view().file_name()

    # Now walk the project directory
    for path, dirs, filenames in self.walk_project_folder(current_file_path):

      # Loop over each file in the directory. Filter by files with a .log extension
        for filename in filter(lambda f: re.search(r"\.(log)$", f), filenames):
          current_file = os.path.join(path, filename)
          if file_matcher.search(current_file):

            # Open the log file
            self.window.open_file(os.path.join(path, filename))
            print("Opened: " + filename)
            return

    print("No " + logfile_name + " log file found")


  def walk_project_folder(self, file_path):
    for folder in self.window.folders():
      if not file_path.startswith(folder):
        continue
      yield from os.walk(folder)
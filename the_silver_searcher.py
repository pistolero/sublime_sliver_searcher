import sublime_plugin
#import sublime
import subprocess


class TheSilverSearcherCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.last_search_string = ''

    def run(self):
        #print ('aaaaa')
        view = self.window.active_view()
        selection_text = view.substr(view.sel()[0])
        self.window.show_input_panel(
            "Search in project:",
            selection_text or self.last_search_string,
            self.perform_search, None, None)        

    def perform_search(self, text):
        view = self.window.new_file()
        folders = [x['path'] for x in self.window.project_data()['folders']]
        view.run_command('do_silver_search', {'text': text, 'folders': folders})
        view.set_read_only(True)
        view.set_scratch(True)
        view.set_syntax_file("Packages/TheSilverSearcher/Find Results.hidden-tmLanguage")
        view.set_name('"%s" search results' % text)


class DoSilverSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, folders):
        self.view.insert(edit, 0, "Searching for '%s'...\n" % text)
        command_line = "ag --line-numbers '%s' %s" % (text, ' '.join(folders))
        ag = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE)        
        pipe = ag.stdout

        output = pipe.read()
        while output:
            self.view.insert(edit, self.view.size(), output.decode('utf-8'))
            output = pipe.read()

        self.view.insert(edit, self.view.size(), u"Done\n")

from tkinter import *
from tkinter import filedialog
import os.path
import os
import re


class App(Frame):
    def __init__(self, master, initialdir="C", filetypes=()):
        super().__init__(master)
        self.filepath = StringVar()
        self.dirpath = StringVar()
        self.error = StringVar()
        self.widget1 = Frame(master)
        self.widget1.pack()
        self._initialdir = initialdir
        self._filetypes = filetypes
        self._create_widgets()
        self._display_widgets()

    def settings():
        root.geometry("640x480")
        root.title("TAPSEP")

    def browse_file(self):
        self.filepath.set(filedialog.askopenfilename(initialdir=self._initialdir, title="Selecionar arquivo",
                                    filetypes=self._filetypes))

    def browse_dir(self):
        self.dirpath.set(filedialog.askdirectory(initialdir=self._initialdir, title="Selecionar pasta"))

    def _create_widgets(self):
        self._label1 = Label(self, text="Selecione o arquivo de entrada e a pasta de saída e clique em iniciar")
        self._button1 = Button(self, text="Procurar", command=self.browse_file)
        self._entry1 = Entry(self, textvariable=self.filepath)
        self._button2 = Button(self, text="Procurar Diretorio", command=self.browse_dir)
        self._entry2 = Entry(self, textvariable=self.dirpath)
        self._button3 = Button(self, text="Iniciar", command=self._cortar_arquivo)
        self._label2 = Label(self, textvariable=self.error)

    def _display_widgets(self):
        self._label1.pack()
        self._button1.pack()
        self._entry1.pack()
        self._button2.pack()
        self._entry2.pack()
        self._button3.pack()
        self._label2.pack()

    def _cortar_arquivo(self):
        fileToSlice = self._entry1.get()
        self.fileCut = open(str(fileToSlice), 'r+')
        dirToSave = self._entry2.get()
        numberFile = 0
        tag_found = False
        self.dirSave = open(os.path.join(str(dirToSave + "/File" + str(numberFile) + ".TAP")), "w")

        try:
            for line in open(str(fileToSlice)):
                if not tag_found:
                    self.dirSave.write(line.strip())
                    self.dirSave.write("\n")
                    print(line.strip())
                    if ('M30' in line.strip()):
                        tag_found = True
                else:
                    remainM30 = line
                    self.dirSave.close()
                    renameaFile = open(os.path.join(str(dirToSave + "/File" + str(numberFile) + ".TAP")), "r+")
                    for i, line in enumerate(renameaFile):
                        if i == 0:
                            newName = line.strip()
                            newName = newName.replace("%_N_", "")
                            newName = newName.replace('_MPF', '')
                            newName = newName.replace('_', ' ')
                            renameaFile.close()
                            os.rename((dirToSave + "/File" + str(numberFile) + ".TAP"), (dirToSave + "/" + newName + ".TAP"))
                            break
                    numberFile = numberFile + 1
                    self.dirSave = open(os.path.join(str(dirToSave + "/File" + str(numberFile) + ".TAP")), "w")
                    self.dirSave.write(remainM30.strip())
                    self.dirSave.write("\n")
                    tag_found = False
                    continue
            self.error.set("OK - Transferidos " + str((numberFile)) + " arquivos")

        except:
            self.error.set("Erro")

        self.dirSave.close()

if __name__ == '__main__':

    root = Tk()

    file_browser = App(root, initialdir="C:/a.txt",
                          filetypes=(('Programas CNC TAP', '*.TAP'),
                                     ("Todos os arquivos", "*.*")))

    file_browser.pack(fill='x', expand=True)

    App(root)
    App.settings()
    root.mainloop()

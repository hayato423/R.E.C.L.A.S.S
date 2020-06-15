import PySimpleGUI as sg


class Other:


  def open(self):
    other_layout = [[sg.Text('other')]]
    other_window = sg.Window('other',layout=other_layout,size=(200,200))
    while True:
      event , value = other_window.read()
      if event is None:
        break
    other_window.close()
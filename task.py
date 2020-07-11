'''
designer:藤野貴裕
date:2020/7/7
purpose:課題詳細画面の表示
'''

import PySimpleGUI as sg

class task:
    def __init__(self,lecture_name,task_name,deadline):
        #授業名、課題名、締切日
        self.lecture_name=lecture_name
        self.task_name=task_name
        self.deadline=deadline

    def open(self):
        #課題詳細画面出力
        layout=[
            [sg.Text('授業名:'+self.lecture_name)],
            [sg.Text('課題名:'+self.task_name)],
            [sg.Text('期限:'+self.deadline)]
        ]
        window = sg.Window(self.lecture_name,layout=layout,size=(200,200))
        while True:
            event ,value = window.read()
            if event is None:
                break
        window.close()

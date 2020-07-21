'''
designer:藤野貴裕
date:2020/7/7
purpose:課題詳細画面の表示
'''

import PySimpleGUI as sg

class Task:
    def __init__(self,lecture_name,task_name,deadline,complete):
    '''課題詳細画面を開き、イベント処理を行う.
    Args:
        lecture_name(str): 授業名
        task_name(str): 課題名
        deadline(str): 締切日
        complete(int): 提出状況
    Returns: なし
    '''
        #授業名、課題名、締切日
        self.lecture_name=lecture_name
        self.task_name=task_name
        self.deadline=deadline[0:4]+'年'+ deadline[4:6] + '月' + deadline[6:8]+'日'
        self.complete = complete

    def open(self):
        #課題詳細画面出力
        layout=[
            [sg.Text('授業名:'+self.lecture_name)],
            [sg.Text('課題名:'+self.task_name)],
            [sg.Text('期限:'+self.deadline)],
            [sg.Text('提出状況'+self.complete)]
        ]
        window = sg.Window(self.lecture_name,layout=layout,size=(300,200))
        while True:
            event ,value = window.read()
            if event is None:
                break
        window.close()

#task = task('1A','1B','20202020','ok')
#task.open(task)
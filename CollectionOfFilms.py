# -*- coding: utf-8 -*-

from tkinter import Tk, Frame, Toplevel, Button, StringVar
from tkinter import GROOVE, FLAT
from tkinter import LEFT, RIGHT
from tkinter import TOP, BOTTOM, CENTER
from tkinter import X, Y

from tkinter.ttk import Label, Scrollbar, Treeview, Entry, Combobox, Style

from sqlite3 import connect


class CollectionOfFilms(Frame): # ГЛАВНЫЙ КЛАСС;
    def __init__(self, root, x, y):
        super().__init__(root)
        self.x = x
        self.y = y
        self.init_main()
        self.db = db
        self.update_records()

    def init_main(self):
        # СТИЛЬ ШРИФТА;
        font_style = ('Consolas', '12')
        
        # СТИЛЬ ТАБЛИЦ и КНОПОК в ВСПЛЫВАЮЩИХ ОКНАХ;
        Style().configure("Treeview.Heading", font=font_style, foreground='#425370')
        Style().configure('Treeview', font=font_style, foreground='#425370')
        Style().configure('TButton', font=('Consolas', '10'))
        Style().configure('TLabel', font=font_style, background='#EDF0F5', foreground='#425370')
        
        # ВЕРХНЯЯ и НИЖНЯЯ ПАНЕЛЬ для КНОПОК и ПОДСКАЗОК;
        TB_TOP = Frame(self, bg='#EDF0F5', bd=1)
        TB_BOT = Frame(self, bg='#EDF0F5', bd=1)
        TB_TOP.pack(side=TOP, fill=X)
        TB_BOT.pack(side=BOTTOM, fill=X)

        # КНОПКИ на ВЕРХНЕЙ ПАНЕЛИ;
        btn_add_ = Button(TB_TOP, text='Добавить', compound=TOP, command=self.open_dlg_add,
                          bg='#EDF0F5', activebackground='#425370', activeforeground='white',
                          width=15, height=1, font=font_style, relief=GROOVE, overrelief=GROOVE)
        btn_edit = Button(TB_TOP, text='Редактировать', compound=TOP, command=self.open_dlg_edit,
                          bg='#EDF0F5', activebackground='#425370', activeforeground='white',
                          width=15, height=1, font=font_style, relief=GROOVE, overrelief=GROOVE)
        btn_del_ = Button(TB_TOP, text='Удалить', compound=TOP, command=self.open_dlg_del,
                          bg='#EDF0F5', activebackground='#425370', activeforeground='white',
                          width=15, height=1, font=font_style, relief=GROOVE, overrelief=GROOVE)
        btn_view = Button(TB_BOT, text='Просмотр', compound=TOP, command=self.open_dlg_view,
                          bg='#EDF0F5', activebackground='#425370', activeforeground='white',
                          width=10, height=1, font=font_style, relief=FLAT, overrelief=FLAT)

        btn_add_.pack(side=LEFT)
        btn_edit.pack(side=LEFT)
        btn_del_.pack(side=RIGHT)
        btn_view.pack(side=RIGHT)

        btn_add_.bind('<Enter>', lambda event: btn_add_.configure(bg='#8E9FBD', fg='white'))
        btn_add_.bind('<Leave>', lambda event: btn_add_.configure(bg='#EDF0F5', fg='black'))
        btn_edit.bind('<Enter>', lambda event: btn_edit.configure(bg='#8E9FBD', fg='white'))
        btn_edit.bind('<Leave>', lambda event: btn_edit.configure(bg='#EDF0F5', fg='black'))
        btn_del_.bind('<Enter>', lambda event: btn_del_.configure(bg='#8E9FBD', fg='white'))
        btn_del_.bind('<Leave>', lambda event: btn_del_.configure(bg='#EDF0F5', fg='black'))
        btn_view.bind('<Enter>', lambda event: btn_view.configure(bg='#8E9FBD', fg='white'))
        btn_view.bind('<Leave>', lambda event: btn_view.configure(bg='#EDF0F5', fg='black'))

        # ВЫВОД ОШИБОК и КОЛ-ВА ЗАПИСЕЙ на НИЖНЮЮ ПАНЕЛЬ;
        self.error = Label(TB_BOT, foreground='red')
        self.count = Label(TB_BOT)
        self.error.pack(side=RIGHT)
        self.count.pack(side=LEFT)

        # ПОЛОСА ПРОКРУТКИ и ТАБЛИЦА;
        _yscroll_ = Scrollbar(self)
        self.tree = Treeview(self, columns=('id', 'name', 'mors', 'janr', 'flag'), height=20, show='headings', yscrollcommand=_yscroll_.set)
        _yscroll_.config(command=self.tree.yview)

        self.tree.column('id',   width=50,  minwidth=50, anchor=CENTER)
        self.tree.column('name', width=370, minwidth=370)
        self.tree.column('mors', width=110, minwidth=110)
        self.tree.column('janr', width=110, minwidth=110)
        self.tree.column('flag', width=140, minwidth=140)

        self.tree.heading('id',   text='№')
        self.tree.heading('name', text='Название')
        self.tree.heading('mors', text='Кино/Сериал')
        self.tree.heading('janr', text='Жанр')
        self.tree.heading('flag', text='Просмотр')

        _yscroll_.pack(side=RIGHT, fill=Y)
        self.tree.pack()
        self.tree.bind('<Button-1>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == 'separator' else None)

    def update_records(self): # ОБНОВЛЕНИЕ ДАННЫХ;
        num = 0
        self.db.c.execute(''' SELECT * FROM films ''')
        [ self.tree.delete(i) for i in self.tree.get_children() ]
        for row in self.db.c.fetchall():
            [ self.tree.insert('', 'end', values=row) ]
            num += 1
        self.count['text'] = ' Количество записей: %d' % (num)

    def add_record(self, name, mors, janr, flag): # ДОБАВЛЕНИЕ;
        if (name != ''):
            self.error['text'] = ''
            flag_record = False
            self.db.c.execute(''' SELECT name FROM films ''')
            for row in self.db.c.fetchall(): # Проверка на схожую запись;
                if (name == row[0]): flag_record = True
            if (not flag_record): self.db.add_data(name, mors, janr, flag)
            else: self.error['text'] = 'Такая запись уже существует! '
        else: self.error['text'] = 'Данные не введены в поле! '
        self.update_records()
    
    def edit_record(self, name, mors, janr, flag): # РЕДАКТИРОВАНИЕ;
        if (name != ''):
            self.error['text'] = ''
            self.db.c.execute(''' UPDATE films SET name=?, mors=?, janr=?, flag=? WHERE id=? ''',
                              (name, mors, janr, flag, self.tree.set(self.tree.selection()[0], '#1')))
        else: self.error['text'] = 'Данные не введены в поле! '
        self.db.conn.commit()
        self.update_records()

    def delete_record(self): # УДАЛЕНИЕ;
        for item in self.tree.selection():
            self.db.c.execute(''' DELETE FROM films WHERE id=? ''', (self.tree.set(item)['id'],))
        self.db.conn.commit()
        self.update_records()

    def open_dlg_add(self): # ОТКРЫВАЕМ ОКНО ДОБАВЛЕНИЯ;
        self.error['text'] = ''
        AddData(self.x, self.y)

    def open_dlg_edit(self): # ОТКРЫВАЕМ ОКНО РЕДАКТИРОВАНИЯ;
        if self.tree.selection():
            self.error['text'] = ''
            EditData(self.x, self.y, self.tree.item(self.tree.selection()[0])['values'][1])
        else: self.error['text'] = 'Не выбрана запись для редактирования! '

    def open_dlg_del(self): # ОТКРЫВАЕМ ОКНО УДАЛЕНИЯ;
        if (self.tree.selection()):
            self.error['text'] = ''
            DeleteData(self.x, self.y)
        else: self.error['text'] = 'Нет записей для удаления! '

    def open_dlg_view(self): # ОТКРЫВАЕМ ОКНО ПРОСМОТРА;
        self.error['text'] = ''
        SelectForViewRecords(self.x, self.y)


class PopupFrameView(Toplevel): # СОРТИРОВКА ФИЛЬМОВ;
    def __init__(self, x, y, *data):
        super().__init__()
        self.x = x
        self.y = y
        self.vr = data
        self.init_frame()
        self.db = db
        self.view = appl
        self.view_record()

    def init_frame(self):
        self.title('Просмотр записей')
        self.geometry('440x392+%d+%d' % (self.x + 180, self.y + 65))
        self.resizable(False, False)

        # НИЖНЯЯ ПАНЕЛЬ для КОЛИЧЕСТВА ЗАПИСЕЙ;
        TB_BOT = Frame(self, bg='#EDF0F5', bd=1)
        TB_BOT.pack(side=BOTTOM, fill=X)

        # ВЫВОД КОЛИЧЕСТВА ЗАПИСЕЙ на НИЖНЮЮ ПАНЕЛЬ;
        self.count = Label(TB_BOT, background='#EDF0F5', foreground='#425370')
        self.count.pack()

        _yscroll_ = Scrollbar(self)
        self.tree = Treeview(self, columns=('id', 'name'), height=18, show='headings', yscrollcommand=_yscroll_.set)
        _yscroll_.config(command=self.tree.yview)
        
        self.tree.column('id',   width=50, anchor=CENTER)
        self.tree.column('name', width=370)
        
        self.tree.heading('id',   text='№')
        self.tree.heading('name', text='Название')

        _yscroll_.pack(side=RIGHT, fill=Y)
        self.tree.pack()
        self.tree.bind('<Button-1>', lambda event: 'break' if self.tree.identify_region(event.x, event.y) == 'separator' else None)

        # УДЕРЖИВАЕМ НАШЕ ДИАЛОГОВОЕ ОКНО 'НА ВЕРХУ';
        self.grab_set()
        self.focus_set()

    def view_record(self): # ПРОСМОТР ОТСОРТИРОВАННЫХ ДАННЫХ;
        num = 0
        if (self.vr[0][0] != '' and self.vr[0][1] == '' and self.vr[0][2] == ''):
            self.db.c.execute(''' SELECT id, name FROM films WHERE mors=? ''', (self.vr[0][0], ))
        if (self.vr[0][0] == '' and self.vr[0][1] != '' and self.vr[0][2] == ''):
            self.db.c.execute(''' SELECT id, name FROM films WHERE janr=? ''', (self.vr[0][1], ))
        if (self.vr[0][0] == '' and self.vr[0][1] == '' and self.vr[0][2] != ''):
            self.db.c.execute(''' SELECT id, name FROM films WHERE flag=? ''', (self.vr[0][2], ))
        if (self.vr[0][0] != '' and self.vr[0][1] != '' and self.vr[0][2] != ''):
            self.db.c.execute(''' SELECT id, name FROM films WHERE mors=? AND janr=? AND flag=? ''', (self.vr[0][0], self.vr[0][1], self.vr[0][2]))
        [ self.tree.delete(i) for i in self.tree.get_children() ]
        for row in self.db.c.fetchall():
            [ self.tree.insert('', 'end', values=row) ]
            num += 1
        self.count['text'] = 'Количество записей: %d' % num


class PopupFrame(Toplevel): # ОПРЕДЕЛЯЕМ ГЛАВНОЕ ОКНО для РАБОТЫ С ДАННЫМИ;
    def __init__(self):
        super().__init__(root)
        self.init_frame()
        self.view = appl

    def init_frame(self):
        self.resizable(False, False)

        # СТИЛЬ ШРИФТА;
        font_style = ('Consolas', '12')

        # НИЖНЯЯ ПАНЕЛЬ ОШИБОК;
        self.TB_M_ = Frame(self, bg='#EDF0F5', bd=1, relief=FLAT)
        self.LBL_1 = Label(self.TB_M_)
        self.TBbtn = Frame(self.TB_M_)
        self.LBL_2 = Label(self.TB_M_)
        self.TB_M_.pack(fill=X)
        self.LBL_1.pack(side=BOTTOM)
        self.TBbtn.pack(side=BOTTOM)
        self.LBL_2.pack(side=BOTTOM)

        # МЕТКИ, ПОЛЕ и РАСКРЫВАЮЩИЕСЯ СПИСКИ;
        kino = [ [ 'Кино', 'Сериал', 'Мультфильм' ],
                 [ 'Боевик', 'Драма', 'Комедия', 'Приключения', 'Триллер', 'Ужасы', 'Фантастика', 'Эротика' ],
                 [ 'Просмотрено', 'Непросмотрено' ] ]
        
        self.L_name = Label(self.TB_M_, text='Название')
        self.L_mors = Label(self.TB_M_, text='Кино/Сериал/Мультфильм')
        self.L_janr = Label(self.TB_M_, text='Жанр')
        self.L_view = Label(self.TB_M_, text='Просмотр')
        self.count_chars = Label(self.TB_M_, font=('Consolas', '7'))
        
        self.len_mx = StringVar() # Максимальная длина символов в поле;
        self.name__ = Entry(self.TB_M_, width=41, font=font_style, textvariable=self.len_mx)
        self.len_mx.trace_variable('w', self.def_max_count_chars)
        self.mors__ = Combobox(self.TB_M_, values=kino[0], width=39, font=font_style, state='readonly')
        self.janr__ = Combobox(self.TB_M_, values=kino[1], width=39, font=font_style, state='readonly')
        self.view__ = Combobox(self.TB_M_, values=kino[2], width=39, font=font_style, state='readonly')

        self.L_name.pack(side=TOP)
        self.name__.pack(side=TOP)
        self.L_mors.pack(side=TOP)
        self.mors__.pack(side=TOP)
        self.L_janr.pack(side=TOP)
        self.janr__.pack(side=TOP)
        self.L_view.pack(side=TOP)
        self.view__.pack(side=TOP)

        self.name__.focus()
        self.mors__.current(0)
        self.janr__.current(0)
        self.view__.current(0)

        # КНОПКА для ЗАКРЫТИЯ ОКНА;
        self.btn_can = Button(self.TBbtn, text='Закрыть', width=25, command=self.destroy)
        self.btn_can.pack(side=RIGHT)
        
        # УДЕРЖИВАЕМ НАШЕ ДИАЛОГОВОЕ ОКНО 'НА ВЕРХУ';
        self.grab_set()
        self.focus_set()

    def def_max_count_chars(self, name, index, mode):
        msg = self.len_mx.get()
        self.count_chars['text'] = '%d/%d' % (len(self.name__.get()), 40)
        if len(msg) > 40:
            self.len_mx.set(msg[:-1])
            #self.len_mx.set(msg[0:39])
            print(self.len_mx.set(msg[0:39]))


class AddData(PopupFrame): # ДОБАВЛЕНИЕ ДАННЫХ;
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.init_add()
        self.view = appl

    def init_add(self):
        self.geometry('400x265+%d+%d' % (self.x + 200, self.y + 100))
        self.title('Добавить запись в Collection Of Films!')
        
        # КНОПКА для ДОБАВЛЕНИЯ;
        btn_add = Button(self.TBbtn, text='Добавить', width=25, command=self.destroy)
        btn_add.pack(side=LEFT)
        btn_add.bind('<Button-1>', lambda event: self.view.add_record(self.name__.get(), self.mors__.get(), self.janr__.get(), self.view__.get()))


class EditData(PopupFrame): # РЕДАКТИРОВАНИЕ ДАННЫХ;
    def __init__(self, x, y, item_select=''):
        super().__init__()
        self.x = x
        self.y = y
        self.item_select = item_select
        self.init_edit()
        self.view = appl

    def init_edit(self):
        self.geometry('400x265+%d+%d' % (self.x + 200, self.y + 100))
        self.title('Редактировать Collection Of Films!')
        self.name__.insert(0, self.item_select) # ДОБАВЛЯЕМ "СТАРУЮ" ЗАПИСЬ в ПОЛЕ;

        # КНОПКА для РЕДАКТИРОВАНИЯ;
        btn_edit = Button(self.TBbtn, text='Редактировать', width=25, command=self.destroy)
        btn_edit.pack(side=LEFT)
        btn_edit.bind('<Button-1>', lambda event: self.view.edit_record(self.name__.get(), self.mors__.get(), self.janr__.get(), self.view__.get()))


class DeleteData(PopupFrame): # УДАЛЕНИЕ ДАННЫХ;
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.init_del()
        self.view = appl

    def init_del(self):
        self.geometry('400x95+%d+%d' % (self.x + 200, self.y + 200))
        self.title('Удалить записи из Collection Of Films!')
        self.L_name['text'] = 'Вы действительно хотите удалить записи?'
        
        # КНОПКА для СОГЛАСИЯ с УДАЛЕНИЕМ ДАННЫХ из БД;
        self.btn_can.config(text='Нет')
        btn_yes = Button(self.TBbtn, text='Да', width=25, command=self.destroy)
        btn_yes.pack(side=LEFT)
        btn_yes.bind('<Button-1>', lambda event: self.view.delete_record())
        
        self.name__.destroy()
        self.count_chars.destroy()
        self.L_mors.destroy()
        self.mors__.destroy()
        self.L_janr.destroy()
        self.janr__.destroy()
        self.L_view.destroy()
        self.view__.destroy()


class SelectForViewRecords(PopupFrame): # ВЫБОР ПУНКТОВ для ПРОСМОТРА ЗАПИСЕЙ;
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.init_del()
        self.view = appl

    def init_del(self):
        self.geometry('400x220+%d+%d' % (self.x + 200, self.y + 100))
        self.title('Выбор Collection Of Films!')
        self.L_name['text'] = 'Поиск по названию'

        # КНОПКА для ПРОСМОТРА ДАННЫХ;
        btn_yes = Button(self.TBbtn, text='Ок', width=25, command=self.destroy)
        btn_yes.pack(side=LEFT)
        btn_yes.bind('<Button-1>', lambda event: PopupFrameView(self.x, self.y, [ self.mors__.get(), self.janr__.get(), self.view__.get() ]))
        
        self.L_name.destroy()
        self.name__.destroy()
        self.count_chars.destroy()


class DataBase: # КЛАСС БАЗЫ ДАННЫХ;
    def __init__(self):
        self.conn = connect('db/films.db')
        self.c = self.conn.cursor()
        self.c.execute(''' CREATE TABLE IF NOT EXISTS films (id integer primary key, name text, mors text, janr text, flag text) ''')
        self.conn.commit()
    
    def add_data(self, name, mors, janr, flag):
        self.c.execute(''' INSERT INTO films(name, mors, janr, flag) VALUES (?, ?, ?, ?) ''', (name, mors, janr, flag))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    root = Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 3.5
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 3.5
    root.title('Collection Of Films')
    root.geometry('800x497+%d+%d' % (x, y))
    root.resizable(False, False)
    db = DataBase()
    appl = CollectionOfFilms(root, x, y)
    appl.pack()
    root.mainloop()

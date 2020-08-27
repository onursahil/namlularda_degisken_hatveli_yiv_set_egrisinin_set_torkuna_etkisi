from tkinter import *

def show_entry_fields():
    print("Mermi Agirligi: %d\nMermi Basinci: %d" % (int(e1.get()), int(e2.get())))

master = Tk()
Label(master, text="Mermi Agirligi").grid(row=0)
Label(master, text="Barut Agirligi").grid(row=1)
Label(master, text="Merminin Namlu Çıkış Hızı").grid(row=2)
Label(master, text="Barutun Verdiği En Yüksek Basınç").grid(row=3)
Label(master, text="Mermi Yolu").grid(row=4)
Label(master, text="Namlu Çapı").grid(row=5)
Label(master, text="Mermi Yarıçapı").grid(row=6)
Label(master, text="Mermi Kutupsal Jirasyon Yarıçapı").grid(row=7)
Label(master, text="Merminin Eksenel Atalet Momenti").grid(row=8)
Label(master, text="Yiv Set Namlu Çıkış Eğimi").grid(row=9)
Label(master, text="Yiv Set Eğrisi n Üssü").grid(row=10)


e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)
e10 = Entry(master)
e11 = Entry(master)

# Input Boxes
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)
e7.grid(row=6, column=1)
e8.grid(row=7, column=1)
e9.grid(row=8, column=1)
e10.grid(row=9, column=1)
e11.grid(row=10, column=1)

Button(master, text='Show', command=show_entry_fields).grid(row=11, column=1, sticky=W, pady=4)

master.mainloop()
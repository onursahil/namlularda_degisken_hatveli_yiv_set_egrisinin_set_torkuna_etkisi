from tkinter import *

# Calculate barrel internal pressure
def namlu_ic_basinci(entry_list):
    barrel_internal_pressure = entry_list[0] + (0.5 * entry_list[1]) / ((2 * entry_list[4]) * )

# Get the input variables from the user
def show_entry_fields():
    # print("Mermi Agirligi: %s\nBarut Agirligi: %s" % (e1.get(), e2.get()))
    mermi_agirligi = float(e1.get())
    barut_agirligi = float(e2.get())
    namlu_cikis_hizi = float(e3.get())
    en_yuksek_basinc = float(e4.get())
    mermi_yolu = float(e5.get())
    namlu_capi = float(e6.get())
    mermi_yaricapi = float(e7.get())
    jirasyon_yaricapi = float(e8.get())
    atalet_momenti = float(e9.get())
    namlu_cikis_egimi = float(e10.get())
    set_egrisi = float(e11.get())

    entry_list = [mermi_agirligi, barut_agirligi, namlu_cikis_hizi, en_yuksek_basinc, mermi_yolu, namlu_capi, mermi_yaricapi, jirasyon_yaricapi, atalet_momenti, namlu_cikis_egimi, set_egrisi]

    namlu_ic_basinci(entry_list)

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
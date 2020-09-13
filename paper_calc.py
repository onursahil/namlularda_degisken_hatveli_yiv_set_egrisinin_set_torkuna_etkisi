from tkinter import *
import math
from generate_heydenreich import gen_heydenreich
from internal_ballistic_factors import ballistic_factors

def entelpolasyon_sum(np, a, b, c, d):
    result = (((np - a) * (d - c)) / (b - a)) + c
    
    return result

def entelpolasyon(np, entry_list, heydenreich_dict):
    np_table = heydenreich_dict['np']
    np_sum = heydenreich_dict['sum_n']
    theta_n = heydenreich_dict['theta_n']
    phi_n = heydenreich_dict['phi_n']
    pi_n = heydenreich_dict['pi_n']
    t_n = heydenreich_dict['t_n']

    for i in range(len(np_table)):
        if np < np_table[i]:
            np_up = np_table[i]
            np_down = np_table[i - 1]

            up_idx = np_table.index(np_up)
            down_idx = np_table.index(np_down)

            break
    
    np_sum_up = np_sum[up_idx]
    np_sum_down = np_sum[down_idx]

    theta_sum_up = theta_n[up_idx]
    theta_sum_down = theta_n[down_idx]

    phi_sum_up = phi_n[up_idx]
    phi_sum_down = phi_n[down_idx]

    pi_sum_up = pi_n[up_idx]
    pi_sum_down = pi_n[down_idx]

    t_sum_up = t_n[up_idx]
    t_sum_down = t_n[down_idx]

    ent_np = entelpolasyon_sum(np, np_down, np_up, np_sum_down, np_sum_up)
    ent_theta = entelpolasyon_sum(np, np_down, np_up, theta_sum_down, theta_sum_up)
    ent_phi = entelpolasyon_sum(np, np_down, np_up, phi_sum_down, phi_sum_up)
    ent_pi = entelpolasyon_sum(np, np_down, np_up, pi_sum_down, pi_sum_up)
    ent_t = entelpolasyon_sum(np, np_down, np_up, t_sum_down, t_sum_up)

    ent_list = [ent_np, ent_theta, ent_phi, ent_pi, ent_t]

    return ent_list

# Piezometrik verim hesaplanmasi
def piezometrik_verim(entry_list, P0):
    np = (P0 / (10 ** 6)) / entry_list[3]
    print("Piezometrik Verim: ", np)
    return np

# Namlu ic basincinin hesaplanmasi
def namlu_ic_basinci(entry_list, A):
    mermi_kutlesi = entry_list[0]
    barut_kutlesi = entry_list[1]
    mermi_yolu = entry_list[4]
    namlu_hizi = entry_list[2]

    mermi_kutlesi = (mermi_kutlesi / (10 ** 3))
    barut_kutlesi = (barut_kutlesi / (10 ** 3))
    mermi_yolu = (mermi_yolu / (10 ** 3))

    P0 = ((mermi_kutlesi + (barut_kutlesi * 0.5)) / (2 * mermi_yolu * A)) * (namlu_hizi ** 2)
    print("Namlu Ic Basinci: ", P0)
    return P0

# Namlu kesit alaninin hesaplanmasi
def namlu_kesit_alani(entry_list):
    D = entry_list[5]
    D = (D / (10 ** 3))
    A = ((math.pi) * (D ** 2)) / 4
    print("Namlu Kesit Alani: ", A)
    return A

# Get the input variables from the user
def show_entry_fields(entry_comps):
    # print("Mermi Agirligi: %s\nBarut Agirligi: %s" % (e1.get(), e2.get()))
    mermi_agirligi = float(e1.get())
    barut_agirligi = float(e2.get())
    namlu_cikis_hizi = float(e3.get())
    en_yuksek_basinc = float(e4.get())
    mermi_yolu = float(e5.get())
    namlu_capi = float(e6.get())
    # mermi_yaricapi = float(e7.get())
    # jirasyon_yaricapi = float(e8.get())
    # atalet_momenti = float(e9.get())
    # namlu_cikis_egimi = float(e10.get())
    # set_egrisi = float(e11.get())

    entry_list = [mermi_agirligi, barut_agirligi, namlu_cikis_hizi, en_yuksek_basinc, mermi_yolu, namlu_capi] #, mermi_yaricapi, jirasyon_yaricapi, atalet_momenti, namlu_cikis_egimi, set_egrisi]

    A = namlu_kesit_alani(entry_list)
    P0 = namlu_ic_basinci(entry_list, A)
    np = piezometrik_verim(entry_list, P0)

    heydenreich_dict = gen_heydenreich()

    ent_list = entelpolasyon(np, entry_list, heydenreich_dict)

    x1 = mermi_yolu * ent_list[0]
    t1 = ((2 * mermi_yolu) / namlu_cikis_hizi) * ent_list[1]
    v1 = namlu_cikis_hizi * ent_list[2]
    pe = (P0 / (10 ** 6)) * ent_list[3]
    te = ((2 * mermi_yolu) / namlu_cikis_hizi) * ent_list[3]

    lmda = mermi_yolu / x1

    for label in master.grid_slaves():
        label.grid_forget()

    for comp in entry_comps:
        comp.destroy()

    Label(master, text="Merminin namlu icinde almis oldugu yol x1: " + str(x1)).grid(row=0)
    Label(master, text="Merminin namlu icinde gecirdigi zaman t1: " + str(t1)).grid(row=1)
    Label(master, text="Mermi Hizi V1: " + str(v1)).grid(row=2)
    Label(master, text="Namlu agzi basinci Pe: " + str(pe)).grid(row=3)
    Label(master, text="Merminin namlu icinde gecirdigi toplam sure Te: " + str(te)).grid(row=4)

    ballistic_chart = ballistic_factors()
    



master = Tk()
n_rows = 7
n_columns = 2
for i in range(n_rows):
    master.grid_rowconfigure(i,  weight = 1)
for i in range(n_columns):
    master.grid_columnconfigure(i,  weight = 1)

Label(master, text="Mermi Agirligi(gr)").grid(row=0)
Label(master, text="Barut Agirligi(gr)").grid(row=1)
Label(master, text="Merminin Namlu Çıkış Hızı(m/s)").grid(row=2)
Label(master, text="Barutun Verdiği En Yüksek Basınç(Mpa)").grid(row=3)
Label(master, text="Mermi Yolu(mm)").grid(row=4)
Label(master, text="Namlu Çapı(mm)").grid(row=5)
# Label(master, text="Mermi Yarıçapı").grid(row=6)
# Label(master, text="Mermi Kutupsal Jirasyon Yarıçapı").grid(row=7)
# Label(master, text="Merminin Eksenel Atalet Momenti").grid(row=8)
# Label(master, text="Yiv Set Namlu Çıkış Eğimi").grid(row=9)
# Label(master, text="Yiv Set Eğrisi n Üssü").grid(row=10)


e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
# e7 = Entry(master)
# e8 = Entry(master)
# e9 = Entry(master)
# e10 = Entry(master)
# e11 = Entry(master)

# Input Boxes
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)
# e7.grid(row=6, column=1)
# e8.grid(row=7, column=1)
# e9.grid(row=8, column=1)
# e10.grid(row=9, column=1)
# e11.grid(row=10, column=1)

entry_comps = [e1, e2, e3, e4, e5, e6]

Button(master, text='Show', command=lambda: show_entry_fields(entry_comps)).grid(row=6, column=1, sticky=W, pady=4)

master.mainloop()
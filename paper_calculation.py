from tkinter import *
import math
from generate_heydenreich import gen_heydenreich
from internal_ballistic_factors import ballistic_factors
import matplotlib.pyplot as plt

def yiv_grafik(x_list, y_list, tork_list):
    plot1 = plt.figure(1)
    plt.title("Yiv Set Mesafesi")
    plt.plot(x_list, y_list)
    plt.xlabel("X Yiv - Set mesafesi (mm)")
    plt.ylabel("Acisal Ivme (rad / s^2)")
    plt.savefig('yiv_set_mesafesi.png')

    plot2 = plt.figure(2)
    plt.title("Setlere Etkiyen Tork")
    plt.plot(x_list, tork_list)
    plt.xlabel("X Yiv - Set mesafesi (mm)")
    plt.ylabel("Tork (Nm)")
    plt.savefig("setlere_etkiyen_tork.png")

    plt.show()
    
    master.quit()

def yiv_hesaplama(x_list, V_list, P_list, yiv_pack):
    for label in master.grid_slaves():
        label.grid_forget()

    for comp in entry_comps:
        comp.destroy()

    mermi_yaricapi = float(yiv_pack[0].get())
    jirasyon_yaricapi = float(yiv_pack[1].get())
    atalet_momenti = float(yiv_pack[2].get())
    cikis_egimi = float(yiv_pack[3].get())
    set_egrisi = float(yiv_pack[4].get())
    kesit_alani = float(yiv_pack[5].get())
    mermi_yolu = float(yiv_pack[6].get())
    mermi_kutlesi = float(yiv_pack[7].get())

    yiv_list = [mermi_yaricapi, jirasyon_yaricapi, atalet_momenti, cikis_egimi, set_egrisi, kesit_alani, mermi_yolu, mermi_kutlesi]

    y_list = []
    tan_alpha = []
    drv_tan = []
    tork_list = []

    for i in range(len(x_list)):
        y_list.append((math.tan(yiv_list[3]) / ((yiv_list[6] / (10 ** 3)) ** (yiv_list[4] - 1))) * ((x_list[i] / (10 ** 3)) ** (yiv_list[4] - 1)))
        tan_alpha.append((math.tan(yiv_list[3]) / (yiv_list[6] / (10 ** 3)) ** (yiv_list[4] - 1)) * (x_list[i] ** (yiv_list[4] - 1)))
        drv_tan.append(((abs(yiv_list[4] - 1) * math.tan(yiv_list[3])) / ((yiv_list[6] / (10 ** 3)) ** abs(yiv_list[4] - 1))) * (x_list[i] ** abs(yiv_list[4] - 2)))
    for i in range(len(V_list)):
        tork_list.append(((yiv_list[7]) * ((yiv_list[1] ** 2) / yiv_list[0])) * (((yiv_list[5] * (P_list[i] * (10 ** 6))) / (yiv_list[7]) * tan_alpha[i]) + ((V_list[i] ** 2) * drv_tan[i])))

    Button(master, text='Yiv Set Grafikleri', command=lambda: yiv_grafik(x_list, y_list, tork_list)).grid(row=6, column=1, sticky=W, pady=4)

def display_x_y(P_list, V_list, t_list, x_list):
    plot1 = plt.figure(1)
    plt.plot(x_list, P_list)
    plt.plot(x_list, V_list)
    plt.xlabel("Mermi Yolu, x, mm")
    plt.ylabel("Basinc, P, MPa")
    plt.savefig("mermi_yolu-basinc.png")

    plot2 = plt.figure(2)
    plt.plot(x_list, t_list)
    plt.xlabel("Mermi Yolu, x, mm")
    plt.ylabel("Zaman, t, ms")
    plt.savefig("mermi_yolu-zaman.png")

    plt.show()

    for label in master.grid_slaves():
        label.grid_forget()

    for comp in entry_comps:
        comp.destroy()

    Label(master, text="Mermi Yarıçapı").grid(row=0)
    Label(master, text="Mermi Kutupsal Jirasyon Yarıçapı").grid(row=1)
    Label(master, text="Merminin Eksenel Atalet Momenti").grid(row=2)
    Label(master, text="Yiv Set Namlu Çıkış Eğimi").grid(row=3)
    Label(master, text="Yiv Set Eğrisi n Üssü").grid(row=4)
    Label(master, text="Namlu Kesit Alani").grid(row=5)
    Label(master, text="Mermi Yolu").grid(row=6)
    Label(master, text="Mermi Kutlesi").grid(row=7)


    e7 = Entry(master)
    e8 = Entry(master)
    e9 = Entry(master)
    e10 = Entry(master)
    e11 = Entry(master)
    e12 = Entry(master)
    e13 = Entry(master)
    e14 = Entry(master)

    e7.grid(row=0, column=1)
    e8.grid(row=1, column=1)
    e9.grid(row=2, column=1)
    e10.grid(row=3, column=1)
    e11.grid(row=4, column=1)
    e12.grid(row=5, column=1)
    e13.grid(row=6, column=1)
    e14.grid(row=7, column=1)

    yiv_pack = [e7, e8, e9, e10, e11, e12, e13, e14]

    Button(master, text='Yiv Set Egrisi Hesaplamalari', command=lambda: yiv_hesaplama(x_list, V_list, P_list, yiv_pack)).grid(row=8, column=1, sticky=W, pady=4)
    

def lambda_entelpolasyon(lmda, ballistic_chart, x1, v1, t1, Pm):
    P_list = []
    V_list = []
    t_list = []
    x_list = []

    lambda_list = ballistic_chart['lambda']
    psi_list = ballistic_chart['psi']
    phi_list = ballistic_chart['phi']
    delta_list = ballistic_chart['delta']

    for i in range(len(lambda_list)):
        if lambda_list[i] <= lmda:
            P_list.append(Pm * psi_list[i])
            V_list.append(v1 * phi_list[i])
            t_list.append(t1 * delta_list[i])
            x_list.append(lambda_list[i] * x1)
    
    return P_list, V_list, t_list, x_list

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
    P_list, V_list, t_list, x_list = lambda_entelpolasyon(lmda, ballistic_chart, x1, v1, t1, en_yuksek_basinc)
    print(P_list, V_list, t_list, x_list)

    Button(master, text='Show Graph', command=lambda: display_x_y(P_list, V_list, t_list, x_list)).grid(row=6, column=1, sticky=W, pady=4)



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


e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)

# Input Boxes
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)

entry_comps = [e1, e2, e3, e4, e5, e6]

Button(master, text='Show', command=lambda: show_entry_fields(entry_comps)).grid(row=6, column=1, sticky=W, pady=4)

master.mainloop()
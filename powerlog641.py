import argparse, sys, lmg641, time, os
import xlsxwriter
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description = "Log measured values from ZES Zimmer LMG641 Power Meter")
    parser.add_argument("val", nargs = '?', help = "Valeurs à mesurer, écrire les valeurs entre guillemets avec un espace entre chaque valeur ex : 'utrms itrms p'")
    parser.add_argument("-lf", "--logfile", dest = "logfile", default='', help = "Nom du fichier qui sera crée")
    parser.add_argument("-host", "--host", dest = "host", default='169.254.6.217', help = "IP address machine")
    parser.add_argument("-d", "--duree", dest="duree", type = int, default=100, help = "Définir la durée de lancement du programme en nb de cycles de mesures")
    parser.add_argument("-v", "--verbose", dest = "verbose", type = int, default=0, help = "Verbose 1 = afficher données")
    parser.add_argument("-i", "--interval", dest="interval", type=float, default=0.01, help = "Interval de mesure en secondes")
    parser.add_argument("-p", "--plot", dest = "plot", type=int, default = 100, help = "Permet de définir la taille de la fenêtre du graphique affiché pendant une mesure")
    parser.add_argument("-a", "--auto", dest = "auto", nargs =2, default= [0.0, 0.0], type = float, help = "Choix de l'interval de mesure [Courant, Tension]")
    args = parser.parse_args()

    if(args.val):
        VAL = args.val.split()
    else:
        VAL = "utrms itrms p".split()
    
    VAL = [v for v in VAL]


    if(args.logfile):
        dossier = args.logfile
        path = os.path.join(dossier, args.logfile)
    else:
        dossier = datetime.now().strftime('%d-%m-%Y_%H-%M-%S') 
        path = os.path.join(dossier, datetime.now().strftime('%d-%m-%Y_%H-%M-%S'))

    os.mkdir(dossier)
    workbook = xlsxwriter.Workbook(path+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column_pixels(0, 6, 100)

    courant = args.auto[0]
    tension = args.auto[1]
    
    print ("connecting to", args.host)
    lmg = lmg641.lmg641(args.host)


    print ("Reset en cours")
    lmg.reset()
    time.sleep(1)

    print ("Connexion réussie :", lmg.read_id()[1])

    print ("Configuration interval")
    lmg.send_short_cmd("CYCL " + str(args.interval));  

    if args.auto != [0.0,0.0]:
        sys.stdout.write("Calibrage manuel activé\n")
        lmg.set_ranges(courant,tension)
    else:
        sys.stdout.write("Calibrage auto activé\n")
    
    lmg.select_values(VAL)

    #log = open(args.logfile, "w")
    i = 0
    row = 1
    #graph = []

    graph = {v: deque(maxlen=args.plot) for v in VAL}

    figure, ax = plt.subplots()
    lines = {v: ax.plot([], [], label=v)[0] for v in VAL}
    ax.legend()
    ax.set_xlabel("Nombre de cycles")
    ax.set_ylabel("Valeurs")
    ax.grid()
    plt.title("Données mesurées")
    boucle = True

    try:
        lmg.cont_on()
        #log.write("--> " + "           ".join(VAL) + "\n")

        for col_val, value in enumerate(VAL):
            worksheet.write(0,col_val, value)
            
        print ("Mesure en cours (press CTRL-C to stop)")
        args.logfile
        print("\nCycles : ")

        if args.verbose == 1:
            sys.stdout.write(str(VAL)+'\n')

        def on_close(event):
            if os.path.exists(str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + ".png"):
                decision = input("\nUn fichier de ce nom existe déjà.\n"
                         "Enregistrer l'image tout de meme ? [o/n] \n"
                         "(Attention si vous décidez d'écraser le fichier le précédent sera remplacé): ")
                if decision == 'n':
                    print("Programme terminé")
                    sys.exit(0)
            elif os.path.exists(args.logfile + ".png"):
                decision = input("\nUn fichier de ce nom existe déjà.\n"
                         "Enregistrer l'image tout de meme ? [o/n] \n"
                         "(Attention si vous décidez d'écraser le fichier le précédent sera remplacé): ")
                if decision == 'n':
                    print("Programme terminé")
                    sys.exit(0)
            figure.savefig(path + ".png")
            nonlocal boucle
            boucle = False
        
        figure.canvas.mpl_connect('close_event', on_close)

       
        while boucle:
             
            data = lmg.read_raw_values()

            if len(data) < len(VAL):
                print("Erreur de data len", data)
                continue
            
          
            for col_i, indice in enumerate(data):
                if col_i < len(VAL):
                    worksheet.write(row, col_i, str(indice).strip().split("\n")[0])
            
            row += 1
            i += 1
            
            worksheet.write(0, 10, "Cycles : "+str(i))

            for v, val in zip(VAL, data):
                valeur = val.strip().split('\n')
                graph[v].append(float(valeur[0]))
                

            #for v in VAL:
                lines[v].set_data(range(len(graph[v])), graph[v])
                
            ax.relim()
            ax.autoscale_view()

            plt.pause(args.interval) 
            
            #data[0] = data[0] + " s" 
            #data[1] = data[1] + " V"
            #data[2] = data[2] + " A"
            #data[3] = data[3] + " V"
            #data[4] = data[4] + " A"
            #data[5] = data[5] + " W"
            #data[6] = data[6] + " A"
            
            if args.verbose == 1:
                sys.stdout.write(" ".join([ str(x) for x in data ]) + "\n") #Output too long
            else:
                sys.stdout.write("\r{0}".format(i) + "/" + str(args.duree))
            sys.stdout.flush()
            #log.write(" ".join([ str(x) for x in data ]) + "\n")
            #col+= 1
            #log.flush()

            if args.duree == i:
                break
           
    except KeyboardInterrupt:
        print

    lmg.cont_off()

    
    #log.close()

    #if graph:
       # plt.figure()

        #for x,y in enumerate(VAL):
         #   plt.plot([d[x] for d in graph if len(d) > x], label=y )
        #plt.legend()
        #plt.xlabel("Nombres de cycles")
        #plt.ylabel("Valeurs")
        #plt.title("Données mesurées")
        #plt.show()
    
    while True:
        try:
            workbook.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            decision = input("Exception caught in workbook.close(): %s\n"
                         "Un fichier de ce nom est déjà ouvert.\n"
                         "Essayez a nouveau d'ecrire le fichier? [o/n] \n"
                         "(Attention si vous décidez d'écraser le fichier le précédent sera remplacé par celui-ci): " % e)
            if decision == 'n':
                print("Programme terminé")
                return
            else: 
                continue
        break


    
    lmg.disconnect()
    print ("\nTerminé", i)


if __name__ == "__main__":
    main()


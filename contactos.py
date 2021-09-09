def contactos(isletdata, delta):
    # contactos alfa-alfa
    contacts_alfas = 0
    # contactos beta-beta
    contacts_betas = 0
    # contactos delta-delta
    contacts_deltas = 0
    # contactos alfa-beta
    contacts_alfas_betas = 0
    # contactos alfas-delta
    contacts_alfas_deltas = 0
    # contactos betas-deltas
    contacts_betas_deltas = 0
    # Matriz de conectividad b-b y b-d
    contact_matrix_bb_bd = []
    # Matriz de conectividad a-a
    contact_matrix_aa = []
    # Matriz de conectividad a-b
    contact_matrix_ab = []
    # Matriz de conetividad a-d
    contact_matrix_ad = []
    # Matriz de conectividad b-b
    contact_matrix_bb = []
    # Matriz de conectividad b-d 
    contact_matrix_bd = []
    # Matriz de conectividad d-d
    contact_matrix_dd = []
    i = 0
    for cell1 in isletdata:
        x1 = cell1[3]
        y1 = cell1[4]
        z1 = cell1[5]
        # bb-bd
        cell1_contact_bb_bd = []
        # aa
        cell1_contact_aa = []
        # ab
        cell1_contact_ab = []
        # ad
        cell1_contact_ad = []
        # bb
        cell1_contact_bb = []
        # bd 
        cell1_contact_bd = []
        # dd
        cell1_contact_dd = []
        j = 0
        for cell2 in isletdata:
            x2 = cell2[3]
            y2 = cell2[4]
            z2 = cell2[5]
            if i == j:
                # bb-bd
                cell1_contact_bb_bd.append(0)
                cell1_contact_aa.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bb.append(0)
                cell1_contact_bd.append(0)
                cell1_contact_dd.append(0)
                j = j + 1
                continue
            d12 = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 + (z2 -z1)**2)
            # betas-betas    
            if (cell1[2] == 12.0 and cell2[2] == 12.0):
                cell1_contact_aa.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bd.append(0)
                cell1_contact_dd.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    cell1_contact_bb_bd.append(1)
                    cell1_contact_bb.append(1)
                    contacts_betas += 1
                else:
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_bb.append(0)
            # alfas-alfas
            elif (cell1[2] == 11.0 and cell2[2] == 11.0):
                cell1_contact_bb_bd.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bb.append(0)
                cell1_contact_bd.append(0)
                cell1_contact_dd.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    contacts_alfas += 1
                    cell1_contact_aa.append(1)
                else:
                    cell1_contact_aa.append(0)
            # deltas-deltas
            elif (cell1[2] == 13.0 and cell2[2] == 13.0):
                cell1_contact_bb_bd.append(0)
                cell1_contact_aa.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bd.append(0)
                cell1_contact_bb.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    contacts_deltas += 1
                    cell1_contact_dd.append(1)
                else:
                    cell1_contact_dd.append(0)
            # betas - deltas
            elif (cell1[2] == 12.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 12.0):
                cell1_contact_aa.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bb.append(0)
                cell1_contact_dd.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    cell1_contact_bb_bd.append(1)
                    contacts_betas_deltas += 1
                    cell1_contact_bd.append(1)
                else:
                    cell1_contact_bb_bd.append(0)
                    cell1_contact_bd.append(0)
            # alfas - betas
            elif (cell1[2] == 11.0 and cell2[2] == 12.0) or (cell1[2] == 12.0 and cell2[2] == 11.0):
                cell1_contact_bb_bd.append(0)
                cell1_contact_aa.append(0)
                cell1_contact_ad.append(0)
                cell1_contact_bb.append(0)
                cell1_contact_dd.append(0)
                cell1_contact_bd.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    contacts_alfas_betas += 1
                    cell1_contact_ab.append(1)
                else:
                    cell1_contact_ab.append(0)
            elif (cell1[2] == 11.0 and cell2[2] == 13.0) or (cell1[2] == 13.0 and cell2[2] == 11.0):
                cell1_contact_bb_bd.append(0)
                cell1_contact_aa.append(0)
                cell1_contact_ab.append(0)
                cell1_contact_bd.append(0)
                cell1_contact_bb.append(0)
                cell1_contact_dd.append(0)
                if cell1[0] + cell2[0] + delta >= d12:
                    contacts_alfas_deltas += 1 
                    cell1_contact_ad.append(1)
                else:
                    cell1_contact_ad.append(0)
            else:
                print('Caso raro')
                #print(str(cell1[2]) + ' , ' + str(cell2[2]))
                #cell1_contact.append(0)
            #print(np.sum(cell1_contact))
            j = j + 1
        #print(np.shape(cell1_contact))
        contact_matrix_bb_bd.append(np.asarray(cell1_contact_bb_bd))
        contact_matrix_aa.append(np.asarray(cell1_contact_aa))
        contact_matrix_ab.append(np.asarray(cell1_contact_ab))
        contact_matrix_ad.append(np.asarray(cell1_contact_ad))
        contact_matrix_bb.append(np.asarray(cell1_contact_bb))
        contact_matrix_bd.append(np.asarray(cell1_contact_bd))
        contact_matrix_dd.append(np.asarray(cell1_contact_dd))
        i = i + 1
    
    contacts_islet = {}
    contacts_islet['bbbd'] = np.stack(np.array(contact_matrix_bb_bd), axis=0)
    contacts_islet['aa'] = np.stack(np.array(contact_matrix_aa), axis=0)
    contacts_islet['ab'] = np.stack(np.array(contact_matrix_ab), axis=0)
    contacts_islet['ad'] = np.stack(np.array(contact_matrix_ad), axis=0)
    contacts_islet['bb'] = np.stack(np.array(contact_matrix_bb), axis=0)
    contacts_islet['bd'] = np.stack(np.array(contact_matrix_bd), axis=0)
    contacts_islet['dd'] = np.stack(np.array(contact_matrix_dd), axis=0)
    #contact_matrix.astype('int')
    contact_count_vec = [contacts_alfas/2, contacts_betas/2, contacts_deltas/2, contacts_alfas_betas/2, contacts_alfas_deltas/2, contacts_betas_deltas/2]
    return [contacts_islet, contact_count_vec]


# Para procesar islote postrocesado
dictconteo, conteo = contactos(isletdata, 1)

# Para guardar diferentes contactos en archivos
np.savetxt('H51_conectividad_bb_bd.txt', dictconteo['bbbd'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_aa.txt', dictconteo['aa'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_ab.txt', dictconteo['ab'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_ad.txt', dictconteo['ad'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_bb.txt', dictconteo['bb'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_bd.txt', dictconteo['bd'], delimiter = '\t', fmt="%d")
np.savetxt('H51_conectividad_dd.txt', dictconteo['dd'], delimiter = '\t', fmt="%d")

# [a-a, b-b, d-d, a-b, a-d, b-d] 
conteo

# total de contactos
np.sum(conteo)
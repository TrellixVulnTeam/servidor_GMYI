from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle, Indenter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.rl_config import defaultPageSize
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import FileResponse
from django.urls import reverse
from reportlab.lib import colors
from datetime import datetime
import locale
from .models import *
from datetime import date
import io
import os
from pathlib import Path
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from num2words import num2words


def cotizacion_pdf_us_df(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    descripcion_cotizacion = cotizacion.descripcion_cotizacion


    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%B %d of %Y ")

    actyear = str(date.today().year)
    sigyear = str(date.today().year + 1)

    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Normal_R',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))



    def myFirstPage(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id,cliente=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        clienteTexto = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleN = styles["Normal_J"]
        styleH4 = styles["Heading4"]
        styleH2 = styles["Heading2"]

        styleRight = styles["Normal_R"]
        styleCB = styles[("Normal_CB")]
        styleB = styles[("Normal_B")]
        styleHB = styles[("Heading1_B")]
        styleHBC = styles[("Heading1_BC")]
        styleNC = styles[("Normal_C")]
        styleNR = styles[("Normal_Red")]
        styleNY = styles[("Normal_Ye")]
        styleNRight = styles[("Normal_Right")]
        styleNBC = styles[("Normal_Center")]
        texto_fecha = ("Tijuana, B.C. at " + dateStr)
        texto_encargado = ("Sincerely " + encargado)
        texto_asunto = ("Subject:")

        p0 = Paragraph(texto_fecha, styleRight)
        p1 = Paragraph(texto_encargado, styleH4)
        p2 = Paragraph(puesto, styleN)
        p3 = Paragraph(clienteTexto, styleH2)
        p4 = Paragraph(texto_asunto, styleH2)
        p5 = Paragraph("""<u>"""+descripcion_cotizacion+"""</u>""", styleCB)
        p6 = Paragraph("Dear Sirs, ", styleN)
        p7 = Paragraph("In relation to your request, we are pleased to present the proposal for the maintenance of the fire detection system. This document presents the economic proposal based on the characteristics of your building and its current equipment in the company. "+nombre+" located in the city of "+lugar_de_mantenimiento, styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("Proposal Index:, ", styleN)
        p9 = Paragraph("1.0 Background", styleN) # aun no se a que se refiere
        p10 = Paragraph("2.0 Scope of job description", styleN)
        p11 = Paragraph("3.0 Summary of economic proposals", styleN)
        p12 = Paragraph("4.0 Terms and Conditions", styleN)
        p13 = Paragraph("1.0 Background", styleHB)  # aun no se a que se refiere
        p14 = Paragraph("The table below shows an overview of the equipment, as well as the annual maintenance visits considered in a calendar year, the quantity column indicates the number of devices considered to be maintained in this economic offer of each type on a regular basis. based either on our recommendation or on the security policies established by the client.", styleN)
        p1extra = Paragraph("Regularly, the additional visits per year are those visits that we propose to carry out in addition to the regular visits, either because they are subject to unusual weather conditions, dust, dirt or chemicals, they can devices in areas under construction, remodeling or the presence of chemicals, if the column is in “0” this means that no zone is being considered as explained above.", styleN)
        p15 = Paragraph("1.1 Preventive maintenance policy", styleHB)
        p16 = Paragraph("To proceed and apply preventive maintenance, it is understood that the fire detection system must be in 100% operation without any failure or problem, if it does not comply, corrective maintenance must first be carried out under an additional budget that is not part of this budget. .", styleN)
        p2extra = Paragraph("Preventive maintenance considers a company commitment to execute a series of actions to the panel and devices in a scheduled manner under an established date in order to maintain the operation of the system at 100% functional from the beginning of the contract date. up to 365 days after signing it.", styleN)
        listdisp = [["Devices","Quantity",Paragraph("visits per year"),Paragraph("Additional visits per year"),Paragraph("Devices in additional periodicity")]]
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
                    listdisp.append(info_disp)

        listadispositivos = ''
        lastdisp = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+'.'

            elif mantenimiento.dispositivo != lastdisp:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","

            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
                    listadispositivos = listadispositivos[:-1]
                    listadispositivos = listadispositivos+"."

        titulo = Nombre_servicio.objects.get(pk=13)
        totaldisp = Mantenimiento.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        p17 = Paragraph("It is considered within the devices to maintain the equipment that currently has being considered "+str(listadispositivos),styleN)
        p3extra = Paragraph("Total Devices: "+str(totaldisp.cantidaddedispositivos), styleN)
        p4extra = Paragraph("The lifting machinery is necessary to be used in devices over 15 feet high, this type of equipment has an associated cost for its transfer to the site and collection, its use per day and it is necessary to recharge under an electrical outlet, this lifting machinery does not It is considered in its cost, so it is the responsibility of the client to request one if necessary for this maintenance work in the visits that are necessary in a scheduled manner, as well as the electrical facilities for recharging the equipment.", styleN)
        p18 = Paragraph("Coverage time "+actyear+"-"+sigyear, styleB)
        p19 = Paragraph("En la siguiente tabla se muestran las actividades que se consideran.",styleB)
        p20 = Paragraph("2.0 Alcance de la descripción del trabajo",styleHB)
        p5extra = Paragraph("Que se Incluye en esta póliza de mantenimiento del sistema de detección de fuego?: ",styleB)
        if cotizacion.periodoregular == 1:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visita de actividades de mantenimiento al año.",styleN,bulletText="•")
        else:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visitas de actividades de mantenimiento al año.",styleN,bulletText="•")
        ppolitica16 = Paragraph("Disponibilidad de portal WEB personalizado para el seguimiento por personal asignado del cliente con todo el Equipo técnico de la empresa para visualización de las actividades de mantenimiento y reportes.",styleN,bulletText="•")
        palcances2 = Paragraph("Poner el sistema en modo de prueba.",styleN,bulletText="•")
        palcances3 = Paragraph("De manera calendarizada cada Visita  se ejecutara la limpieza de los sensores y módulos físicamente. Los dispositivos para limpiar dando mayor jerarquía  son los que determine el reporte de mantenimiento y sensibilidad que indique un nivel de suciedad mayor al 35% después se procede con el resto.",styleN,bulletText="•")
        palcances4 = Paragraph("Limpieza de panel de alarmas ( pantalla LCD, conectores, terminales de cableado, limpieza, sellos silicón, revisión de conectividad a panel remoto y actividad en el Lazo SLC de dispositivos).",styleN,bulletText="•")
        palcances5 = Paragraph("Reporte de sensibilidad el cual nos indica que sensor está sucio de sus elementos internos para proceder a limpiarlos.",styleN,bulletText="•")
        palcances6 = Paragraph("Limpieza de estrobos-cornetas y palancas.",styleN,bulletText="•")
        palcances7 = Paragraph("Prueba de verificación de leds del panel , iluminar todos los leds.",styleN,bulletText="•")
        palcances8 = Paragraph("Prueba de verificación de energía primaria, remover energía de AC, verificar que el panel funcione con baterías, verificar que el panel entre en modo de problema, restablecer energía y dejar todo en orden en modo normal.",styleN,bulletText="•")

        palcances9 = Paragraph("Prueba de señales de problema en panel  funcionen apropiadamente",styleN,bulletText="•")
        palcances10 = Paragraph("Verificación bimestral que la pantalla LCD del panel marque la hora apropiada.",styleN,bulletText="•")
        p6extra = Paragraph("""<u>¿Que no se incluye?:</u>""",styleB)


        palcances12= Paragraph("Equipos y Refacciones.",styleN,bulletText="1.")
        palcances13= Paragraph("Materiales como cables o tuberías.",styleN,bulletText="2.")
        palcances14= Paragraph("Maquinaria de elevación.",styleN,bulletText="3.")
        palcances15= Paragraph("Trabajos en días Festivos",styleN,bulletText="4.")
        palcances16= Paragraph("Trabajos fuera del horario establecido.",styleN,bulletText="5.")
        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Servicio de soporte técnico -Horas de servicios generales adicionales":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')


        ppolitica = Paragraph("2.1 Política de apoyo técnico y diagnóstico",styleHB)
        ppoliticaextra1=Paragraph("""<u>¿Que se Incluye en las horas de Servicios de soporte Técnico, pruebas y servicios de reparación consideradas en esta propuesta?:</u>""",styleB)
        ppolitica1 = Paragraph("Servicio de soporte técnico para diagnostico o corrección por "+str(suma_horas)+" horas o 12 meses, lo que suceda primero.  ",styleN,bulletText="•")
        ppolitica2 = Paragraph("Días regular para Soporte técnico de Lunes a sábado (horarios de 8.00am – 6:00pm)",styleN,bulletText="•")
        ppolitica3 = Paragraph("Atención técnica y reparación de fallas en los paneles o en los dispositivos en su red.",styleN,bulletText="•")
        ppolitica4 = Paragraph("Tiempo de respuesta de servicios normal: siguiente día hábil.",styleN,bulletText="•")
        ppolitica5 = Paragraph("Prueba semestral de palancas manuales, inspección visual, activar el mecanismo y confirmar respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica6 = Paragraph("Prueba semestral de detectores de calor, inspección visual, conducir una función de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica7 = Paragraph("Prueba anual de detectores de humo, conducir una función de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica8 = Paragraph("Prueba semestral de todos los dispositivos de iniciación de alarmas, activar los dispositivos y verificar que los circuitos de aplicación de notificación apropiados estén funcionando correctamente (NAC) así como información de zona y mensajes correspondientes, abrir el cableado de campo de los dispositivos de iniciación y verificar que el mensaje de problema se indique en el panel.",styleN,bulletText="•")
        ppolitica9 = Paragraph("Prueba anual de Notificación en cornetas-estrobos, colocar el panel en alarma, drill o modo de prueba y verificar que todos los notificadores estén trabajando apropiadamente.",styleN,bulletText="•")
        ppolitica10 = Paragraph("Prueba de energía secundaria en los paneles principales y remotos, remover energía primaria de AC, medir corrientes en modo “stand by” y  alarmado y comparar con cálculo de baterías para verificar una capacidad de batería adecuada, probar a plena carga por 5 minutos, medir voltajes de baterías a plena carga, restablecer energía primaria de AC al final de la prueba, restablecer y cerrar panel al final de la prueba.",styleN,bulletText="•")
        ppolitica11 = Paragraph("Mano de obra por remplazo de cualquier refacción como módulos, sensores, tarjetas, paneles, fuentes de poder, cables",styleN,bulletText="•")
        listadispositivospol = ''
        lastdisppol = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+'.'

            elif mantenimiento.dispositivo != lastdisppol:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+","

            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivos+" "+str(mantenimiento.dispositivo)+","
                    listadispositivospol = listadispositivospol[:-1]
                    listadispositivospol = listadispositivospol+"."


        ppolitica12 = Paragraph("Tiempo de  Programación y configuración de Paneles  sobre los equipos dentro de la póliza de mantenimiento.",styleN,bulletText="•")
        #ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoeléctricos, fuentes de poder, módulos de control. Monitores de flujo, resistencias de fin de línea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Atención a Emergencias en caso de falla total del panel principal y que la operación del 50% o mas del sistema este comprometida con un tiempo de respuesta en sitio de 4 hora.",styleN,bulletText="•")
        ppolitica16 = Paragraph("Los costos asociados de un dispositivo dañado será tomado en cuenta de la lista de precios que se proporciona en este documento en conjunto con el contrato, de esta manera cuando un dispositivo se dañen la facturación de la refacción sea en base a este precio.",styleN)



        table_dis = Table(listdisp, colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento",Paragraph("Acts. de mmnto por año"),
                            Paragraph("Acts. adicionales")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte técnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]

                td_mantenimientos.append(data_mantenimientos)
        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total de horas de servicio de soporte técnico incluidas en esta poliza","Horas",suma_horas]]
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        preciofinal = 0
        preciofinalincadicional = 0
        for mantenimiento in mantenimientos:
            preciofinal = preciofinal + mantenimiento.costomantenimientoregular
            preciofinalincadicional = preciofinalincadicional + mantenimiento.costomantenimientoregular + mantenimiento.costomantenimientoadicional
        preciofinal = float(round(preciofinal))
        preciofinal1 = num2words(preciofinal, to="currency", lang='es', currency='USD').upper()
        preciofinal = "${:,.2f}".format(preciofinal)
        preciofinalincadicional = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicional)

        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Description", "Quantity", "Unit", "Cost"]]
        td_precioadicional = [["Description", "Quantity", "Unit", "Cost"]]
        data_precio = [Paragraph("Annual maintenance contract fee"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinal),styleNC)]
        data_precioadicional = [Paragraph("Annual maintenance contract fee including additional periodicity"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            td_precioadicional.append(data_precioadicional)
            table_preadicional = Table(td_precioadicional)
            table_preadicional.setStyle(ts_pre)
            ppreciotextoadicional = Paragraph(preciofinalincadicional1+" USD + IVA",styleNBC)
            p22adicional = Paragraph(actyear+"-"+sigyear+" Regular operational maintenance and annual technical support including additional periodicity",styleB)
            p23adicional = Paragraph("Total Economic Proposal for Preventive Maintenance including additional periodicity",styleHBC)
            p24adicional = Paragraph("Maintenance policy "+actyear+"-"+sigyear+".............................{}".format(preciofinalincadicional),styleNY)
            p25adicional = Paragraph(preciofinalincadicional1+" USD + IVA",styleNY)

        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        p21 = Paragraph("3.0 Summary of the economic proposal", styleHB)
        p22 = Paragraph(actyear+"-"+sigyear+" Regular operational maintenance and annual technical support",styleB)


        p23 = Paragraph("Total Economic Proposal for Preventive Maintenance",styleHBC)
        p24 = Paragraph("Maintenance policy "+actyear+"-"+sigyear+".............................{}".format(preciofinal),styleNY)
        p25 = Paragraph(preciofinal1+" USD + IVA",styleNY)

        ptitulotermino = Paragraph("4.0 Terms and Conditions", styleHB)
        pterminos1 = Paragraph("Prices quoted are expressed in US dollars.",styleN,bulletText="-")
        pterminos2 = Paragraph("The IVA of 16% not included.",styleN,bulletText="-")
        pterminos3 = Paragraph("The exchange rate will be that of Banco BBVA for sale at the window in force on the day of the effective payment operation. PAYMENTS ARE NOT ACCEPTED USING THE EXCHANGE RATE OF THE OFFICIAL GAZETTE OF THE FEDERATION.", styleN, bulletText="-")
        pterminos4 = Paragraph("Offer valid: 30 calendar days, after which prices are subject to change without notice.",styleN,bulletText="-")
        pterminos5 = Paragraph("The process begins by confirming your total payment or advance payment, as the case may be, and your purchase order placement.",styleN,bulletText="-")
        #pterminos6 = Paragraph("Para proceder con el mantenimiento correctivo, es necesario cubrir la póliza anual al 100% en el primer día de atención.",styleN,bulletText="-")
        pterminos7 = Paragraph(
            "To proceed with preventive maintenance, it is necessary to cover the annuity of the policy at 100% on the first day of the first scheduled visit.", styleN, bulletText="-")
        pterminos8 = Paragraph("The indicated prices are offered by the Total of the Proposal quoted here, any change in conditions or selected equipment must be quoted again.",styleN,bulletText="-")
        pterminos9 = Paragraph("Delivery time: coordinate with the operations area to assign the date and time of execution, this date should not be greater than 7 calendar days after receipt of payment for the policy.",styleN,bulletText="-")

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("End of document", styleNC)
        pregards = Paragraph("Regards",styleNC)
        pdanieljara = Paragraph(nombrecontitulo,styleNC)
        pdirector = Paragraph(puesto,styleNC)

        Story.append(p0)
        Story.append(p1)
        Story.append(p2)
        Story.append(p3)
        Story.append(p4)
        Story.append(p5)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p6)
        Story.append(pblank)
        Story.append(p7)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #Segunda pagina
        Story.append(p13)
        Story.append(p14)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(pblank)
        Story.append(p1extra)
        Story.append(PageBreak())

        #Tercera pagina
        Story.append(p15)
        Story.append(pblank)
        Story.append(p16)
        Story.append(pblank)
        Story.append(p2extra)
        Story.append(pblank)
        Story.append(p17)
        Story.append(pblank)
        Story.append(p3extra)
        Story.append(pblank)
        Story.append(p4extra)
        Story.append(PageBreak())

        #Cuarta pagina
        Story.append(p18)
        Story.append(p19)
        Story.append(pblank)
        Story.append(table_man)
        Story.append(table_tot)
        Story.append(pblank)
        Story.append(PageBreak())

        #Quinta pagina
        Story.append(p20)
        Story.append(pblank)
        Story.append(p5extra)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(palcances2)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(pblank)
        Story.append(p6extra)
        Story.append(pblank)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances14)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(pblank)

        Story.append(PageBreak())


        Story.append(ppolitica)
        Story.append(ppoliticaextra1)
        Story.append(pblank)
        Story.append(ppolitica1)
        Story.append(ppolitica16)
        Story.append(ppolitica2)
        Story.append(ppolitica3)
        Story.append(ppolitica4)
        Story.append(ppolitica5)
        Story.append(ppolitica6)
        Story.append(ppolitica7)
        Story.append(ppolitica8)
        Story.append(ppolitica9)
        Story.append(ppolitica10)
        Story.append(ppolitica11)
        Story.append(ppolitica12)
        # Story.append(ppolitica13)
        Story.append(ppolitica14)


        Story.append(PageBreak())

        #Sexta pagina
        Story.append(p21)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p22)
        Story.append(pblank)
        Story.append(table_pre)
        Story.append(ppreciotexto)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p23)
        Story.append(p24)
        Story.append(p25)
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pblank)
            Story.append(p22adicional)
            Story.append(pblank)
            Story.append(table_preadicional)
            Story.append(ppreciotextoadicional)
            Story.append(pblank)
            Story.append(pblank)
            Story.append(p23adicional)
            Story.append(p24adicional)
            Story.append(p25adicional)
            Story.append(pblank)
            Story.append(pblank)

        Story.append(PageBreak())

        #Septima pagina
        Story.append(ptitulotermino)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        #Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pterminos9)
        Story.append(pblank)
        Story.append(pfin)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pregards)
        Story.append(pdanieljara)
        Story.append(pdirector)





        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_fuego_{}.pdf'.format(nombre))

def cotizacion_pdf_us_cctv(request, cliente_id, cotizacion_id, usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion_CCTV.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    # cambios area de mantenimiento
    area_de_mantenimiento = cotizacion.area_de_mantenimiento
    # cambios
    descripcion_cotizacion = cotizacion.descripcion_cotizacion

    #locale.setlocale(locale.LC_TIME, 'es-ES')
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%B %d of %Y ")

    actyear = str(date.today().year)
    sigyear = str(date.today().year + 1)

    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Normal_R',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))



    def myFirstPage(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        mantenimientos = Mantenimiento_CCTV.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion_CCTV.objects.get(pk=cotizacion_id,cliente=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        clienteTexto = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleN = styles["Normal_J"]
        styleH4 = styles["Heading4"]
        styleH2 = styles["Heading2"]

        styleRight = styles["Normal_R"]
        styleCB = styles[("Normal_CB")]
        styleB = styles[("Normal_B")]
        styleHB = styles[("Heading1_B")]
        styleHBC = styles[("Heading1_BC")]
        styleNC = styles[("Normal_C")]
        styleNR = styles[("Normal_Red")]
        styleNY = styles[("Normal_Ye")]
        styleNRight = styles[("Normal_Right")]
        styleNBC = styles[("Normal_Center")]
        texto_fecha = ("Tijuana, B.C. at " + dateStr)
        texto_encargado = ("Sincerely " + encargado)
        texto_asunto = ("Subject:")

        p0 = Paragraph(texto_fecha, styleRight)
        p1 = Paragraph(texto_encargado, styleH4)
        p2 = Paragraph(puesto, styleN)
        p3 = Paragraph(clienteTexto, styleH2)
        p4 = Paragraph(texto_asunto, styleH2)
        p5 = Paragraph("""<u>"""+descripcion_cotizacion+"""</u>""", styleCB)
        p6 = Paragraph("Dear Sirs, ", styleN)
        #cambios para area de mantenimiento
        p7 = Paragraph("In relation to your request, we present the associated costs of the preventive maintenance service of the Closed Circuit Television system for "+nombre+" in the area of "+str(area_de_mantenimiento)+" located in "+lugar_de_mantenimiento, styleN)
        #cambios
        p7extra2 = Paragraph("To apply preventive maintenance it is important that the system is in operation, without failures, otherwise corrective maintenance would be applied and then preventive maintenance would proceed.", styleN)
        p7extra3 = Paragraph("It is considered a preventive maintenance policy with a duration of 12 months", styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("Proposal Index:, ", styleN)
        p9 = Paragraph("1.0 Background.", styleN)
        p10 = Paragraph("2.0 Scope of work.", styleN)
        p11 = Paragraph("3.0 Price and Payment Methods.", styleN)
        p12 = Paragraph("4.0 Price outside the maintenance contract.", styleN)
        pAntecedentes1 = Paragraph("""<u>1.0 Background</u>""", styleB)
        pAntecedentes2 = Paragraph("The total devices considered for maintenance are the following:",styleN)
        listdisp = [["Device","Quantity",Paragraph("visits per year"),Paragraph("Additional visits per year"),Paragraph("Devices in additional periodicity")]]
        mantenimientos = Mantenimiento_CCTV.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
                    listdisp.append(info_disp)

        listadispositivos = ''
        lastdisp = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+'.'

            elif mantenimiento.dispositivo != lastdisp:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","

            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
                    listadispositivos = listadispositivos[:-1]
                    listadispositivos = listadispositivos+"."

        titulo = Nombre_servicio_CCTV.objects.get(pk=5)
        totaldisp = Mantenimiento_CCTV.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        titulofirmware = Nombre_servicio_CCTV.objects.get(pk=7)
        totaldispfirmware = Mantenimiento_CCTV.objects.get(titulonombre = titulofirmware,cotizacion=cotizacion_id,cliente=cliente_id)
        titulosoftware = Nombre_servicio_CCTV.objects.get(pk=21)
        totaldispsoftware = Mantenimiento_CCTV.objects.get(titulonombre = titulosoftware,cotizacion=cotizacion_id,cliente=cliente_id)
        pAntecedentes3 = Paragraph("Total Devices: "+str(totaldisp.cantidaddedispositivos), styleN)
        pAntecedentes4 = Paragraph("Total devices with Firmware update: "+str(totaldispfirmware.cantidaddedispositivos), styleN)
        pAntecedentes5 = Paragraph("Total devices with Software License update: "+str(totaldispsoftware.cantidaddedispositivos), styleN)

        palcances0 = Paragraph("""<u>2.0 Scope of work</u>""",styleB)
        palcances1 = Paragraph("Preventive maintenance scope of work:",styleN)
        palcances2 = Paragraph("""<u>what is included?:</u>""",styleB)
        meses = int(12 / cotizacion.periodoregular)
        if cotizacion.periodoregular == 1:
            palcances3 = Paragraph("On a scheduled basis, the cleaning of the equipment mentioned above will be carried out every {} months with a total of {} events per year.".format(meses,cotizacion.periodoregular),styleN,bulletText="1.")
        else:
            palcances3 = Paragraph("On a scheduled basis, the cleaning of the equipment mentioned above will be carried out every {} months with a total of {} events per year.".format(meses,cotizacion.periodoregular),styleN,bulletText="1.")
        palcances4 = Paragraph("Cleaning of Video Recording Equipment",styleN,bulletText="2.")
        palcances5 = Paragraph("Cleaning of all CCTV devices.",styleN,bulletText="3.")
        palcances6 = Paragraph("Review of real-time video transmission to the monitor.",styleN,bulletText="4.")
        palcances7 = Paragraph("Review of the video of the monitor, it is verified that it has good brightness and contrast.",styleN,bulletText="5.")
        palcances8 = Paragraph("Review of power sources and their operation.",styleN,bulletText="6.")
        palcances9 = Paragraph("If a damaged device is detected, the associated costs will be quoted independently and installed with prior authorization from the client.",styleN,bulletText="7.")
        palcances10 = Paragraph("Scope of work of emergency maintenance:",styleN,bulletText="8.")
        palcances11 = Paragraph("Technical Support 5 days a week (Monday to Friday from 8:00 a.m. to 5:00 p.m.).",styleN,bulletText="•")

        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Help Desk Service -Additional General Service Hours":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')

        palcances12 = Paragraph(str(suma_horas)+" hours of annual technical service or 12 months, whichever comes first for attention to on-site failures.",styleN,bulletText="•")
        palcances13 = Paragraph("Repair services, diagnostics, adjustments and updates.",styleN,bulletText="•")
        palcances15 = Paragraph("Camera Device Firmware Update, NVR.",styleN,bulletText="•")
        palcances16 = Paragraph("If applicable Workstation (PC) Cleanup Client and display server.",styleN,bulletText="•")
        palcances17 = Paragraph("""<u>What is excluded?:</u>""",styleB)
        palcances18= Paragraph("Update of operating systems or patches on Workstations and servers.",styleN,bulletText="1.")
        palcances19= Paragraph("Parts such as cables, cameras, sources, nvr. (If needed, they will be quoted in writing and will be installed with the prior authorization of the client).",styleN,bulletText="2.")
        palcances20= Paragraph("Elevation Machinery if it is not indicated that it is considered within the cost.",styleN,bulletText="3.")

        listadispositivospol = ''
        lastdisppol = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+'.'

            elif mantenimiento.dispositivo != lastdisppol:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+","

            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivos+" "+str(mantenimiento.dispositivo)+","
                    listadispositivospol = listadispositivospol[:-1]
                    listadispositivospol = listadispositivospol+"."


        table_dis = Table(listdisp,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Maintenance",Paragraph("Maintenance activities per year"),
                            Paragraph("Additional activities")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte técnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]
                    td_mantenimientos.append(data_mantenimientos)

            elif str(mantenimiento.titulonombre) == "Servicio de soporte técnico -Horas de servicios generales adicionales":
                costohorasservicio = mantenimiento.costototal

        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total hours of technical support service included in this policy","Hours",suma_horas]]
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        preciofinal = 0
        preciofinalincadicional = 0
        for mantenimiento in mantenimientos:
            preciofinal = preciofinal + mantenimiento.costomantenimientoregular
            preciofinalincadicional = preciofinalincadicional + mantenimiento.costomantenimientoregular + mantenimiento.costomantenimientoadicional
        preciofinal = float(round(preciofinal))
        preciofinal1 = num2words(preciofinal, to="currency", lang='es', currency='USD').upper()
        preciofinaltexto = "${:,.2f}".format(preciofinal)
        preciofinalincadicionalnum = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicionalnum)

        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Description","Quantity","Unit","Cost"]]
        td_precioadicional = [["Description","Quantity","Unit","Cost"]]

        data_precio = [Paragraph("Annual maintenance contract fee"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinaltexto),styleNC)]
        data_precioadicional = [Paragraph("Annual maintenance contract fee including additional periodicity"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)

        preciommto = preciofinal - costohorasservicio
        preciommto = float(round(preciommto))
        costohorasservicio = float(round(costohorasservicio))
        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)

        pprecio1 = Paragraph("""<u>3.0 Price and method of payment:</u>""",styleB)
        pprecio2 = Paragraph("Preventive maintenance of equipment:             $ {} USD".format(preciommto),styleN)
        pprecio3 = Paragraph("Equipment Emergency Services Hours:     $ {} USD".format(costohorasservicio),styleN)
        pprecio4 = Paragraph("Total price for annual maintenance",styleN)
        pprecio6 = Paragraph("""<u>Total price for annual maintenance payable per event          $ {} USD</u>""".format(preciofinal),styleCB)
        pprecio7 = Paragraph("The payment is each event, it must be settled before the maintenance is carried out.",styleNC)

        if cotizacion.periodoregular == 1:
            preciocuatri = float(round(preciofinal))
            pprecio8 = Paragraph("Annual payment in a single installment: $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 2:
            preciocuatri = float(round(preciofinal/2))
            pprecio8 = Paragraph("Annual payment in two installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 3:
            preciocuatri = float(round(preciofinal/3))
            pprecio8 = Paragraph("Annual payment in three installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 4:
            preciocuatri = float(round(preciofinal/4))
            pprecio8 = Paragraph("Annual payment in four installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 6:
            preciocuatri = float(round(preciofinal/6))
            pprecio8 = Paragraph("Annual payment in six installments:  $ {} USD + IVA".format(preciocuatri),styleN)

        preciocuatritexto = num2words(preciocuatri, to="currency", lang='es', currency='USD')
        pprecio9 = Paragraph("({} USD + IVA)".format(preciocuatritexto),styleN)

        #Precio para mantenimientos con periodicidad adicional
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            pprecioadicional1 = Paragraph("Total price for annual maintenance including additional periodicities",styleN)
            pprecioadicional2 = Paragraph("""<u>Total price for annual maintenance payable per event including additional periodicities          {} USD</u>""".format(preciofinalincadicional),styleCB)
            pprecioadicional3 = Paragraph("The payment is each event, it must be settled before the maintenance is carried out.",styleNC)
            precioadicionalcuatritexto = num2words(preciofinalincadicionalnum, to="currency", lang='es', currency='USD')

            if cotizacion.periodoregular == 1:
                precioadicionalcuatri = preciofinalincadicionalnum
                pprecioadicional14 = Paragraph("Annual payment in a single installment: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 2:
                precioadicionalcuatri = preciofinalincadicionalnum/2
                pprecioadicional14 = Paragraph("Annual payment in two installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 3:
                precioadicionalcuatri = preciofinalincadicionalnum/3
                pprecioadicional14 = Paragraph("Annual payment in three installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 4:
                precioadicionalcuatri = preciofinalincadicionalnum/4
                pprecioadicional14 = Paragraph("Annual payment in four installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 6:
                precioadicionalcuatri = preciofinalincadicionalnum/6
                pprecioadicional14 = Paragraph("Annual payment in six installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)

            pprecioadicional15 = Paragraph("({} USD + IVA)".format(precioadicionalcuatritexto),styleN)

        pprecio10 = Paragraph("""<u>Commercial terms:</u>""",styleB)
        pprecio11 = Paragraph("The prices mentioned above are expressed in US Dollars and do not include VAT.",styleN,bulletText="•")
        pprecio12 = Paragraph("To proceed with the service, it is necessary to be covered by the policy on the first day of the month in which the maintenance will be carried out.. ",styleN,bulletText="•")
        pprecio13 = Paragraph("If the payment is made in pesos, its exchange rate will be in relation to the banking institution of purchase from Santander or BBVA, confirm before.",styleN,bulletText="•")


        pterminos0 = Paragraph("""<u>4.0 Price outside the maintenance contract:</u>""",styleB)
        pterminos1 = Paragraph("Hourly costs from 8am to 5pm is $65.00 DLL per hour per technician.",styleN,bulletText="1.")
        pterminos2 = Paragraph("Hourly costs from 8:00 am to 5:00 pm is $126.00 DLL per hour per engineer.",styleN,bulletText="2.")
        pterminos3 = Paragraph("The cost per hour at these times is $90.00 USD per technician and $190.00 USD per engineer: Monday to Friday from 6:00pm to 7am, Saturdays from 1pm to 11:59pm, Sundays from 00:00 to 11:59pm. billing service from the visit for review, analysis, problem identification and solution. ",styleN,bulletText="3.")
        pterminos4 = Paragraph("Support via telephone to support staff of {} for the attention of an event which hesitates to be able to solve them, they are supported for 30 minutes in case of not being resolved, a technician is sent to the site at an additional cost to the client. Cost of technical support via telephone $35.50 USD per event. Technical support hours from 8:00 a.m. to 5:00 p.m. without emergency number.".format(cliente),styleN,bulletText="4.")
        pterminos5 = Paragraph("In case of failure of the devices and the equipment has to be replaced, the reflected cost will be the associated time of the technical staff in evaluation and diagnosis, plus the cost of spare parts plus shipping costs if they apply in guarantees, returns, etc.",styleN,bulletText="5.")
        pterminos6 = Paragraph("The prices mentioned above are expressed in US Dollars and do not include VAT. ",styleN,bulletText="-")
        pterminos7 = Paragraph("Billing for services is presented by event. ",styleN,bulletText="-")
        pterminos8 = Paragraph("Without further ado for the moment and waiting for any clarification in this regard, I remain yours. ",styleN,bulletText="-")
        pterminosatentamente = Paragraph("Sincerely",styleNC)

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("End of document",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pnombrecontitulo = Paragraph(nombrecontitulo,styleNC)
        ppuesto = Paragraph(puesto,styleNC)


        #Portada
        Story.append(p0)
        Story.append(p1)
        Story.append(p2)
        Story.append(p3)
        Story.append(p4)
        Story.append(p5)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p6)
        Story.append(pblank)
        Story.append(p7)
        Story.append(pblank)
        Story.append(p7extra2)
        Story.append(pblank)
        Story.append(p7extra3)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #1.0 Antecedentes
        Story.append(pAntecedentes1)
        Story.append(pAntecedentes2)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(pblank)
        Story.append(pAntecedentes3)
        Story.append(pAntecedentes4)
        Story.append(pAntecedentes5)
        Story.append(pblank)
        Story.append(PageBreak())

        #2.0 Alcances de los trabajos
        Story.append(palcances0)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances2)
        Story.append(pblank)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(Indenter("1cm"))
        Story.append(palcances11)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(Indenter("-1cm"))
        Story.append(palcances17)
        Story.append(pblank)
        Story.append(palcances18)
        Story.append(palcances19)
        Story.append(palcances20)
        Story.append(pblank)
        Story.append(PageBreak())

        #3.0 Precio y forma de pago
        Story.append(pprecio1)
        Story.append(pblank)
        Story.append(pprecio2)
        Story.append(pprecio3)
        Story.append(pblank)
        Story.append(pprecio4)
        Story.append(pblank)
        Story.append(pprecio6)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pprecio7)
        Story.append(pblank)
        Story.append(pprecio8)
        Story.append(pprecio9)
        Story.append(pblank)
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pprecioadicional1)
            Story.append(pblank)
            Story.append(pprecioadicional2)
            Story.append(pblank)
            Story.append(pprecioadicional3)
            Story.append(pblank)
            Story.append(pprecioadicional14)
            Story.append(pprecioadicional15)
            Story.append(pblank)
        Story.append(pprecio10)
        Story.append(pblank)
        Story.append(pprecio11)
        Story.append(pprecio12)
        Story.append(pprecio13)
        Story.append(pblank)
        Story.append(PageBreak())

        #4.0 precio fuera del contrato
        Story.append(pterminos0)
        Story.append(pblank)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pblank)
        Story.append(pfin)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pterminosatentamente)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pnombrecontitulo)
        Story.append(ppuesto)





        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_cctv_{}.pdf'.format(nombre))

def cotizacion_pdf_ca(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion_CA.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    descripcion_cotizacion = cotizacion.descripcion_cotizacion

    #locale.setlocale(locale.LC_TIME, 'es-ES')
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%B %d of %Y ")

    actyear = str(date.today().year)
    sigyear = str(date.today().year + 1)

    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Normal_R',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))


    def myFirstPage(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        mantenimientos = Mantenimiento_CA.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion_CA.objects.get(pk=cotizacion_id,cliente=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        clienteTexto = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleN = styles["Normal_J"]
        styleH4 = styles["Heading4"]
        styleH2 = styles["Heading2"]

        styleRight = styles["Normal_R"]
        styleCB = styles[("Normal_CB")]
        styleB = styles[("Normal_B")]
        styleHB = styles[("Heading1_B")]
        styleHBC = styles[("Heading1_BC")]
        styleNC = styles[("Normal_C")]
        styleNR = styles[("Normal_Red")]
        styleNY = styles[("Normal_Ye")]
        styleNRight = styles[("Normal_Right")]
        styleNBC = styles[("Normal_Center")]
        texto_fecha = ("Tijuana, B.C. at " + dateStr)
        texto_encargado = ("Sincerely. " + encargado)
        texto_asunto = ("Case:")

        p0 = Paragraph(texto_fecha, styleRight)
        p1 = Paragraph(texto_encargado, styleH4)
        p2 = Paragraph(puesto, styleN)
        p3 = Paragraph(clienteTexto, styleH2)
        p4 = Paragraph(texto_asunto, styleH2)
        p5 = Paragraph("""<u>"""+descripcion_cotizacion+"""</u>""", styleCB)
        p6 = Paragraph("Dear Sirs, ", styleN)
        p7 = Paragraph("In relation to your request, we present the associated costs of the preventive maintenance service of the Access Control system for "+nombre+" located in "+lugar_de_mantenimiento, styleN)
        p7extra2 = Paragraph("To apply preventive maintenance it is important that the system is in operation, without failures, otherwise corrective maintenance would be applied and then preventive maintenance would proceed.", styleN)
        p7extra3 = Paragraph("It is considered a preventive maintenance policy with a duration of 12 months", styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("Proposal Index:, ", styleN)
        p9 = Paragraph("1.0 Background.", styleN)
        p10 = Paragraph("2.0 Scope of work.", styleN)
        p11 = Paragraph("3.0 Price and Payment Methods.", styleN)
        p12 = Paragraph("4.0 Price outside the maintenance contract.", styleN)
        pAntecedentes1 = Paragraph("""<u>1.0 Background</u>""", styleB)
        pAntecedentes2 = Paragraph("The total devices considered for maintenance are the following:",styleN)
        listdisp = [["Device","Quantity",Paragraph("visits per year"),Paragraph("Additional visits per year"),Paragraph("Devices in additional periodicity")]]
        mantenimientos = Mantenimiento_CA.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
                    listdisp.append(info_disp)

        # listadispositivos = ''
        # lastdisp = listdisp[-1]

        # for mantenimiento in mantenimientos:
        #     if len(listdisp) == 1:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+'.'

        #     elif mantenimiento.dispositivo != lastdisp:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","

        #     else:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
        #             listadispositivos = listadispositivos[:-1]
        #             listadispositivos = listadispositivos+"."

        titulo = Nombre_servicio_CA.objects.get(pk=1)
        totaldisp = Mantenimiento_CA.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        titulofirmware = Nombre_servicio_CA.objects.get(pk=3)
        totaldispfirmware = Mantenimiento_CA.objects.get(titulonombre = titulofirmware,cotizacion=cotizacion_id,cliente=cliente_id)
        pAntecedentes3 = Paragraph("Total Devices: "+str(totaldisp.cantidaddedispositivos), styleN)
        pAntecedentes4 = Paragraph("Total devices with firmware update: "+str(totaldispfirmware.cantidaddedispositivos), styleN)

        palcances0 = Paragraph("""<u>2.0 Scope of work</u>""",styleB)
        palcances1 = Paragraph("Preventive maintenance scope of work:",styleN)
        palcances2 = Paragraph("""<u>what is included?:</u>""",styleB)
        meses = int(12 / cotizacion.periodoregular)
        if cotizacion.periodoregular == 1:
            palcances3 = Paragraph("On a scheduled basis, the cleaning of the aforementioned equipment will be carried out every {} months with a total of {} events per year.".format(meses,cotizacion.periodoregular),styleN,bulletText="•")
        else:
            palcances3 = Paragraph("On a scheduled basis, the cleaning of the aforementioned equipment will be carried out every {} months with a total of {} events per year.".format(meses,cotizacion.periodoregular),styleN,bulletText="•")
        palcances4 = Paragraph("Cleaning of PCs, workstations and servers.",styleN,bulletText="•")
        palcances5 = Paragraph("Cleaning of power supplies and controllers, modules and cabinets.",styleN,bulletText="•")
        palcances6 = Paragraph("Review of your IP and RS-485 communications.",styleN,bulletText="•")
        palcances7 = Paragraph("Review of the video of the monitor, it is verified that it has good brightness and contrast.",styleN,bulletText="•")
        palcances8 = Paragraph("Review of batteries, modules and rectifiers of power sources.",styleN,bulletText="•")
        palcances9 = Paragraph("Update of access manager software and firmware in controller equipment.",styleN,bulletText="•")
        palcances10 = Paragraph("Software update of new service pack or change of versions in operating system.",styleN,bulletText="•")
        palcances11 = Paragraph("Data communication tests of PC equipment, servers and controllers.",styleN,bulletText="•")
        palcances12 = Paragraph("Implementation of updates to the current version, version changes and tests for management and monitoring software.",styleN,bulletText="•")
        palcances13 = Paragraph("Adjustments and corrections of door accessories such as exit button, magnets, readers, door status sensors.",styleN,bulletText="•")
        palcances14 = Paragraph("Verification of correct operation of the integration with elevator control and, where appropriate, necessary corrections.",styleN,bulletText="•")
        palcances15 = Paragraph("Verification and updates of correlations between access doors and associated video channel.",styleN,bulletText="•")
        palcances16 = Paragraph("Technical Support 5 days a week (Monday to Friday from 8:00 a.m. to 5:00 p.m.).",styleN,bulletText="•")

        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Help Desk Service -Additional General Service Hours":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')

        palcances17 = Paragraph(str(suma_horas)+" hours of annual technical service or 12 months, whichever comes first for attention to on-site failures.",styleN,bulletText="•")
        palcances18 = Paragraph("""<u>what is included?:</u>""",styleB)
        palcances19= Paragraph("Does not include lifting machinery, if necessary it will be quoted independently.",styleN,bulletText="•")
        palcances20= Paragraph("Spare parts not included.",styleN,bulletText="•")
        palcances21= Paragraph("Note: If a damaged device is detected, the associated costs will be quoted independently and installed with the prior authorization of the client, in case of applying a guarantee, it will not cost more than those associated for shipping and returning to the manufacturer.",styleN)

        listadispositivospol = ''
        lastdisppol = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+'.'

            elif mantenimiento.dispositivo != lastdisppol:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+","

            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+","
                    listadispositivospol = listadispositivospol[:-1]
                    listadispositivospol = listadispositivospol+"."


        ppolitica12 = Paragraph("Programming time and configuration of Panels on the equipment within the maintenance policy.",styleN,bulletText="•")
        #ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoeléctricos, fuentes de poder, módulos de control. Monitores de flujo, resistencias de fin de línea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Attention to Emergencies in case of total failure of the main panel and that the operation of 50% or more of the system is compromised with a response time on site of 4 hours.",styleN,bulletText="•")
        ppolitica16 = Paragraph("The associated costs of a damaged device will be taken into account from the price list that is provided in this document together with the contract, in this way when a device is damaged, the billing of the spare part will be based on this price.",styleN)



        table_dis = Table(listdisp,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Maintenance",Paragraph("Maintenance activities per year"),
                            Paragraph("Additional activities")
                            ,Paragraph("Execution time")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte técnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]
                td_mantenimientos.append(data_mantenimientos)
            elif str(mantenimiento.titulonombre) == "Servicio de soporte técnico -Horas de servicios generales adicionales":
                costohorasservicio = mantenimiento.costototal

        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total hours of technical support service included in this policy","Hours",suma_horas]]
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        preciofinal = 0
        preciofinalincadicional = 0
        for mantenimiento in mantenimientos:
            preciofinal = preciofinal + mantenimiento.costomantenimientoregular
            preciofinalincadicional = preciofinalincadicional + mantenimiento.costomantenimientoregular + mantenimiento.costomantenimientoadicional
        preciofinal = float(round(preciofinal))
        preciofinal1 = num2words(preciofinal, to="currency", lang='es', currency='USD').upper()
        preciofinaltexto = "${:,.2f}".format(preciofinal)
        preciofinalincadicionalnum = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicionalnum)

        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Description","Quantity","Unit","Cost"]]
        td_precioadicional = [["Description","Quantity","Unit","Cost"]]

        data_precio = [Paragraph("Annual maintenance contract fee"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinal),styleNC)]
        data_precioadicional = [Paragraph("Annual maintenance contract fee including additional periodicity"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)

        costohorasservicio = float(round(costohorasservicio))
        preciommto = preciofinal - costohorasservicio
        preciommto = float(round(preciommto))
        costohorasservicio = float(round(costohorasservicio))
        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        pprecio1 = Paragraph("""<u>3.0 Precio y forma de pago:</u>""",styleB)
        pprecio2 = Paragraph("Mantenimiento preventivo de equipos:             $ {} USD".format(preciommto),styleN)
        pprecio3 = Paragraph("Horas de Servicios de emergencia de equipos:     $ {} USD".format(costohorasservicio),styleN)
        pprecio4 = Paragraph("Precio total por mantenimiento anual",styleN)
        pprecio6 = Paragraph("""<u>Precio total por mantenimiento anual pagadero por evento          $ {} USD</u>""".format(preciofinal),styleCB)
        pprecio7 = Paragraph("El pago es cada evento, debe estar liquidado antes de efectuarse el mantenimiento.",styleNC)

        if cotizacion.periodoregular == 1:
            preciocuatri = float(round(preciofinal))
            pprecio8 = Paragraph("Annual payment in a single installment: $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 2:
            preciocuatri = float(round(preciofinal/2))
            pprecio8 = Paragraph("Annual payment in a two installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 3:
            preciocuatri = float(round(preciofinal/3))
            pprecio8 = Paragraph("Annual payment in three installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 4:
            preciocuatri = float(round(preciofinal/4))
            pprecio8 = Paragraph("Annual payment in four installments:  $ {} USD + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 6:
            preciocuatri = float(round(preciofinal/6))
            pprecio8 = Paragraph("Annual payment in six installments:  $ {} USD + IVA".format(preciocuatri),styleN)

        preciocuatritexto = num2words(preciocuatri, to="currency", lang='es', currency='USD')
        pprecio9 = Paragraph("({} USD + IVA)".format(preciocuatritexto),styleN)

        #Precio para mantenimientos con periodicidad adicional
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            pprecioadicional1 = Paragraph("Total price for annual maintenance including additional periodicities",styleN)
            pprecioadicional2 = Paragraph("""<u>Total price for annual maintenance payable per event including additional periodicities          {} USD</u>""".format(preciofinalincadicional),styleCB)
            pprecioadicional3 = Paragraph("The payment is each event, it must be settled before the maintenance is carried out.",styleNC)
            precioadicionalcuatritexto = num2words(preciofinalincadicionalnum, to="currency", lang='es', currency='USD')

            if cotizacion.periodoregular == 1:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum))
                pprecioadicional14 = Paragraph("Annual payment in a single installment: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 2:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/2))
                pprecioadicional14 = Paragraph("Annual payment in a two installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 3:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/3))
                pprecioadicional14 = Paragraph("Annual payment in three installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 4:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/4))
                pprecioadicional14 = Paragraph("Annual payment in four installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 6:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/6))
                pprecioadicional14 = Paragraph("Annual payment in six installments: $ {} USD + IVA".format(precioadicionalcuatri),styleN)

            pprecioadicional15 = Paragraph("({} USD + IVA)".format(precioadicionalcuatritexto),styleN)

        pprecio10 = Paragraph("""<u>Commercial terms:</u>""",styleB)
        pprecio11 = Paragraph("The prices mentioned above are expressed in US Dollars and do not include VAT..",styleN,bulletText="•")
        pprecio12 = Paragraph("To proceed with the service, it is necessary to be covered by the policy on the first day of the month in which the maintenance is performed. ",styleN,bulletText="•")
        pprecio13 = Paragraph("If the payment is made in pesos, its exchange rate will be in relation to the banking institution of purchase from Santander or BBVA, confirm before.",styleN,bulletText="•")


        pterminos0 = Paragraph("""<u>4.0 Price outside the maintenance contract:</u>""",styleB)
        pterminos1 = Paragraph("Hourly costs from 8am to 5pm is $66.00 DLL per hour per technician.",styleN,bulletText="1.")
        pterminos2 = Paragraph("Hourly costs from 8:00 am to 5:00 pm is $135.00 DLL per hour per engineer.",styleN,bulletText="2.")
        pterminos3 = Paragraph("The cost per hour during these hours is $90.00 USD per technician and $190.00 USD per engineer.: ",styleN,bulletText="3.")
        pterminos4 = Paragraph("Monday to Friday from 6:00pm to 7am",styleN)
        pterminos5 = Paragraph("Saturdays from 1pm to 11:59pm ",styleN)
        pterminos6 = Paragraph("Sundays from 00:00 to 11:59pm",styleN)
        pterminos7 = Paragraph("The service costs are billed from the visit for the review, analysis, problem identification and solution.",styleN)
        pterminos8 = Paragraph("Support via telephone to support staff of {} for the attention of an event which hesitates to be able to solve them, they are supported for 30 minutes in case of not being resolved, a technician is sent to the site at an additional cost to the client. Cost of technical support via telephone $35.50 USD per event. Technical support hours from 8:00 a.m. to 5:00 p.m. without emergency number.".format(cliente),styleN,bulletText="4.")
        pterminos9 = Paragraph("In case of failure of the devices and the equipment has to be replaced, the reflected cost will be the associated time of the technical personnel involved, spare parts + shipping costs if they apply in guarantees, returns, etc.",styleN,bulletText="5.")
        pterminos10 = Paragraph("The prices mentioned above are expressed in US Dollars and do not include VAT..",styleN)
        pterminosatentamente = Paragraph("Sincerely",styleNC)

        if cotizacion.periodoregular == 1:
            pextra1 = Paragraph("The annual maintenance billing will be presented in an annual exhibition and will be payable before the date of execution of the maintenance event.",styleN)
        elif cotizacion.periodoregular == 2:
            pextra1 = Paragraph("The annual maintenance billing will be presented in two semi-annual installments and will be payable before the date of execution of the maintenance event.",styleN)
        elif cotizacion.periodoregular == 3:
            pextra1 = Paragraph("The billing of the annual maintenance will be presented in three quarterly installments and will be payable before the date of execution of the maintenance event.",styleN)
        elif cotizacion.periodoregular == 4:
            pextra1 = Paragraph("Annual maintenance billing will be presented in four quarterly installments and will be payable prior to the maintenance event execution date.",styleN)
        elif cotizacion.periodoregular == 6:
            pextra1 = Paragraph("The annual maintenance billing will be presented in six bi-monthly installments and will be payable before the date of execution of the maintenance event.",styleN)

        pextra2 = Paragraph("Billing for services outside the policy is presented per event. ",styleN)
        pextra3 = Paragraph("Without further ado for the moment and waiting for any clarification in this regard, I remain up to you.",styleN)

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("End of document",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pnombrecontitulo = Paragraph(nombrecontitulo,styleNC)
        ppuesto = Paragraph(puesto,styleNC)

        #Portada
        Story.append(p0)
        Story.append(p1)
        Story.append(p2)
        Story.append(p3)
        Story.append(p4)
        Story.append(p5)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p6)
        Story.append(pblank)
        Story.append(p7)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p7extra2)
        Story.append(pblank)
        Story.append(p7extra3)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #1.0 Antecedentes
        Story.append(pAntecedentes1)
        Story.append(pAntecedentes2)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(pblank)
        Story.append(pAntecedentes3)
        Story.append(pAntecedentes4)
        Story.append(pblank)
        Story.append(PageBreak())

        #2.0 Alcances de los trabajos
        Story.append(palcances0)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances2)
        Story.append(pblank)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(palcances11)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances14)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(palcances17)
        Story.append(pblank)
        Story.append(palcances18)
        Story.append(pblank)
        Story.append(palcances19)
        Story.append(palcances20)
        Story.append(pblank)
        Story.append(palcances21)
        Story.append(pblank)
        Story.append(PageBreak())

        #3.0 Precio y forma de pago
        Story.append(pprecio1)
        Story.append(pblank)
        Story.append(pprecio2)
        Story.append(pprecio3)
        Story.append(pblank)
        Story.append(pprecio4)
        Story.append(pblank)
        Story.append(pprecio6)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pprecio7)
        Story.append(pblank)
        Story.append(pprecio8)
        Story.append(pprecio9)
        Story.append(pblank)
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pprecioadicional1)
            Story.append(pblank)
            Story.append(pprecioadicional2)
            Story.append(pblank)
            Story.append(pprecioadicional3)
            Story.append(pblank)
            Story.append(pprecioadicional14)
            Story.append(pprecioadicional15)
            Story.append(pblank)
        Story.append(pprecio10)
        Story.append(pblank)
        Story.append(pprecio11)
        Story.append(pprecio12)
        Story.append(pprecio13)
        Story.append(pblank)
        Story.append(PageBreak())

        #4.0 precio fuera del contrato
        Story.append(pterminos0)
        Story.append(pblank)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pterminos9)
        Story.append(pterminos10)
        Story.append(pblank)
        Story.append(pextra1)
        Story.append(pextra2)
        Story.append(pextra3)
        Story.append(pblank)
        Story.append(pfin)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pterminosatentamente)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pnombrecontitulo)
        Story.append(ppuesto)

        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_ca_{}.pdf'.format(nombre))
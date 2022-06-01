import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class FestividadesEcuador(HolidayBase):
    """
    Una clase para representar un dia festivo en Ecuador por provincias(FestividadesEcuador)
    El objetivo es determinar si una fecha especifica es un dia festivo de la manera mas rapida y flexible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Estos se hereran de la clase HolidayBase)
    ----------
    prov: str
        Codigo de provincia según  ISO3166-2
    Metodos:
    -------
    __init__(self, placa, fecha, hora, en_linea=False):
        
        Construye todos los atributos necesarios para el objeto FestividadesEcuador.
    _Es_Festivo(self, fecha):
        Retorna si una fecha es festiva o no.
    """     
    # ISO 3166-2 codigos para las principal subdivision, 
    # llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCIAS = ["EC-P"]  # TODO añadir mas provincias

    def __init__(self, **kwargs):
        """
        Contruye todos los atributos necesarios para el objeto FestividadesEcuador
        """         
        self.pais = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _Es_Festivo(self, año):
        """
        chequear si la fecha es festivo o no.
                
        Parametros
        ----------
        fecha : str
            año de una fecha
        Retorna
        -------
        Retorna verdadero si una fecha es una dia festivo caso contrario retorna falso.
        """                    
        # Año nuevo
        self[datetime.date(año, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(año, DEC, 25)] = "Navidad [Christmas]"
        
        # Semana Santa
        self[easter(año) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) ]"
        self[easter(año)] = "Día de Pascuas"
        
        # Carnaval
        total_lent_days = 46
        self[easter(año) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval "
        self[easter(año) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval"
        
        # Dia del trbajador
        name = "Día Nacional del Trabajo"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if año > 2015 and datetime.date(año, MAY, 1).weekday() in (5,1):
            self[datetime.date(año, MAY, 1) - datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif año > 2015 and datetime.date(año, MAY, 1).weekday() == 6:
            self[datetime.date(año, MAY, 1) + datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, MAY, 1) + rd(weekday=FR)] = name
        else:
            self[datetime.date(año, MAY, 1)] = name
        
        # Batalla del Pichincha, las reglas son de la misma manera que el dia del trabajo.
        name = "Batalla del Pichincha"
        if año > 2015 and datetime.date(año, MAY, 24).weekday() in (5,1):
            self[datetime.date(año, MAY, 24).weekday() - datetime.timedelta(days=1)] = name
        elif año > 2015 and datetime.date(año, MAY, 24).weekday() == 6:
            self[datetime.date(año, MAY, 24) + datetime.timedelta(days=1)] = name
        elif año > 2015 and  datetime.date(año, MAY, 24).weekday() in (2,3):
            self[datetime.date(año, MAY, 24) + rd(weekday=FR)] = name
        else:
            self[datetime.date(año, MAY, 24)] = name        
        
        # Primer grito de la indepencia, las reglas son las mismas que las del dia del trabajo.
        name = "Primer Grito de la Independencia "
        if año > 2015 and datetime.date(año, AUG, 10).weekday() in (5,1):
            self[datetime.date(año, AUG, 10)- datetime.timedelta(days=1)] = name
        elif año > 2015 and datetime.date(año, AUG, 10).weekday() == 6:
            self[datetime.date(año, AUG, 10) + datetime.timedelta(days=1)] = name
        elif año > 2015 and  datetime.date(año, AUG, 10).weekday() in (2,3):
            self[datetime.date(año, AUG, 10) + rd(weekday=FR)] = name
        else:
            self[datetime.date(año  , AUG, 10)] = name       
        
        # Guayaquil's independence, the rules are the same as the labor day
        name = "Independencia de Guayaquil [Guayaquil's Independence]"
        if año > 2015 and datetime.date(año, OCT, 9).weekday() in (5,1):
            self[datetime.date(año, OCT, 9) - datetime.timedelta(days=1)] = name
        elif año > 2015 and datetime.date(año, OCT, 9).weekday() == 6:
            self[datetime.date(año, OCT, 9) + datetime.timedelta(days=1)] = name
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, OCT, 9) + rd(weekday=FR)] = name
        else:
            self[datetime.date(año, OCT, 9)] = name        
        
        # Dia de difuntos
        namedd = "Día de los difuntos" 
        # Independencia de  Cuenca
        nameic = "Independencia de Cuenca"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en días corridos,
        #se aplicarán las siguientes reglas:
        if (datetime.date(año, NOV, 2).weekday() == 5 and  datetime.date(año, NOV, 3).weekday() == 6):
            self[datetime.date(año, NOV, 2) - datetime.timedelta(days=1)] = namedd
            self[datetime.date(año, NOV, 3) + datetime.timedelta(days=1)] = nameic     
        elif (datetime.date(año, NOV, 3).weekday() == 2):
            self[datetime.date(año, NOV, 2)] = namedd
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(año, NOV, 3).weekday() == 3):
            self[datetime.date(año, NOV, 3)] = nameic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = namedd
        elif (datetime.date(año, NOV, 3).weekday() == 5):
            self[datetime.date(año, NOV, 2)] =  namedd
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(año, NOV, 3).weekday() == 0):
            self[datetime.date(año, NOV, 3)] = nameic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = namedd
        else:
            self[datetime.date(año, NOV, 2)] = namedd
            self[datetime.date(año, NOV, 3)] = nameic  
            
        # Fundacion de Quito, aplica solo para la provincia de Pichincha.
        # las reglas son las mismas que el dia del trabajo.
        name = "Fundación de Quito"        
        if self.prov in ("EC-P"):
            if año > 2015 and datetime.date(año, DEC, 6).weekday() in (5,1):
                self[datetime.date(año, DEC, 6) - datetime.timedelta(days=1)] = name
            elif año > 2015 and datetime.date(año, DEC, 6).weekday() == 6:
                self[(datetime.date(año, DEC, 6).weekday()) + datetime.timedelta(days=1)] =name
            elif año > 2015 and  datetime.date(año, DEC, 6).weekday() in (2,3):
                self[datetime.date(año, DEC, 6) + rd(weekday=FR)] = name
            else:
                self[datetime.date(año, DEC, 6)] = name

class PicoPlaca:
    """
    Una clase para representar un vehículo.
    Medida de restricción (Pico y Placa)
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    atributos
    ----------
    placa : str 
        El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
        caracteres que identifican e individualizan el vehículo respecto de los demás;
        
        El formato usado es:
        XX-YYYY o XXX-YYYY, 
        donde X la letra capital y la Y es un digito.
    fecha : str
        Fecha en la que el vehículo pretende transitar
        siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
    hora : str
       tiempo en que el vehículo pretende transitar
        siguiendo el formato
        HH:MM: Ejemplo, 08:35, 19:30
    en_linea: boolean, Opcional
        Si esta en linea == Verdadero se utilizará la API de días festivos abstractos
    Metodos
    -------
    __init__(self, placa, fecha, hora, EnLinea=falso):
        Construir todos los tributos necesarios
        para el objeto PicoPlaca.
    placa(self):
        Consigue los valores del atributo placa
    placa(self, valor):
        Configura el valor del atributo placa
    fecha(self):
        Obetiene el valor del atributo fecha
    fecha(self, valor):
        configura el valor del atributo fecha
    hora(self):
        obtiene el valor del atributo hora.
    hora(self, valor):
        configural valor del atributo hora
    __buscar_dia(self, fecha):
        retorna el dia de la fecha
    __Es_Hora_Pico(self, hora):
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
    __Es_Feriado:
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
    predecir (auto):
        Devuelve True si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora especificadas, de lo contrario, False
    """ 
    #Dias de la semana
    __dias = [
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo"]

    # Diccionario que contiene la informacion de los dias de restricciones.
    __restriciones = {
            "Lunes": [1, 2],
            "Martes": [3, 4],
            "Miercoles": [5, 6],
            "Jueves": [7, 8],
            "Viernes": [9, 0],
            "Sabado": [],
            "Domingo": []}

    def __init__(self, placa, fecha, hora, En_Linea):
        """
        Construye todos los atributos para el objeto PIcoPlaca
                
        Parametros
        ----------
            placa : str 
                El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
                caracteres que identifican e individualizan el vehículo respecto de los demás;
                El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito.
            fecha : str
                Fecha en la que el vehículo pretende transitar
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
            hora : str
                time in which the vehicle intends to transit
                It is following the format HH:MM: e.g., 08:35, 19:30
            en_linea: boolean, opcional
                si esta en linea == Verdadero se utilizará la API de días festivos abstractos (el valor predeterminado es Falso)
        """                
        self.placa = placa
        self.fecha = fecha
        self.hora    = hora
        self.En_Linea = En_Linea


    @property
    def placa(self):
        """Obtiene el valor del atributo placa"""
        return self._placa


    @placa.setter
    def placa(self, valor):
        """
        Establece el valor al atributo placa
        Parametros
        ----------
        valor : str
        
        Plantear
        ------
        ValorError
            si la cadena de  valor no tiene formato
            XX-YYYY o XXX-YYYY, 
            Donde X es una letra mayuscula y Y is un digito.
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', valor):
            raise ValueError(
                'La placa debe estar en el siguiente formato:XX-YYYY o XXX-YYYY, Donde X es una letra mayuscula y Y es un digito.')
        self._placa = valor


    @property
    def Fecha(self):
        """Obtiene el valor del atributo fecha."""
        return self._fecha


    @Fecha.setter
    def Fecha(self, Valor):
        """
        Establece el valor del atributo fecha.
        Parametros
        ----------
        valor : Cadena
        
        Plantear
        ------
        ValorError
            Si la cadena de valor no tiene el formato: YYYY-MM-DD (Ej.: 2021-04-02)
        """
        try:
            if len(Valor) != 10:
                raise ValueError
            datetime.datetime.strptime(Valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)')
        self._date = Valor
        

    @property
    def hora(self):
        """Obtiene el valor del atributo Hora"""
        return self._hora


    @hora.setter
    def hora(self, valor):
        """
        Establece el valor del atributo hora
        Parametros
        ----------
        valor : cadena
        
        Plantear
        ------
        ValorError
            Si el valor de la cadena no tiene el formato: HH:MM (Ej., 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', valor):
            raise ValueError(
                'Si el valor de la cadena no tiene el formato: HH:MM (Ej., 08:31, 14:22, 00:01)')
        self._time = valor


    def __Buscar_dia(self, fecha):
        """
        Buscar el dia de la fecha: ej., Miercoles
        Parametros
        ----------
        fecha : cadena
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        retorna
        -------
        Retrona el dia de la fecha como una cadena
        """        
        d = datetime.datetime.strptime(fecha, '%Y-%m-%d').weekday()
        return self.__days[d]


    def _Es_Hora_Pico(self, hora):
        """
        Comprueba si el tiempo proporcionado está dentro de las horas pico prohibidas,
        donde las horas pico son: 07:00 - 09:30 y 16:00 - 19:30
        Parámetros
        ----------
        Hora : Cadena
            Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        Devoluciones
        -------
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """           
        t = datetime.datetime.strptime(hora, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __Es_Festivo(self, Fecha, En_Linea):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
        si en línea == Verdadero, utilizará una API REST, de lo contrario, generará los días festivos del año examinado
        
        Parámetros
        ----------
        fecha: calle
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        en línea: booleano, opcional
            si en línea == Verdadero, se utilizará la API de días festivos abstractos
        Devoluciones
        -------
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """            
        y, m, d = Fecha.split('-')

        if En_Linea:
            # API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            # 1 solicitud por segundo
            # recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave de API.
                raise requests.HTTPError(
                    'Falta la clave API. Guarde su clave en la variable de entorno HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones obtenemos una matriz vacía
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_Festividades = FestividadesEcuador(prov='EC-P')
            return Fecha in ecu_Festividades


    def predecir(self):
        """
        Comprueba si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora proporcionada según las reglas de Pico y Placa:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
        Devoluciones
        -------
        Devoluciones
        Verdadero si el vehículo con
        la placa especificada puede estar en el camino
        en la fecha y hora especificadas, de lo contrario Falso
        """
        # Comprobar si la fecha es un día festivo
        if self.__Es_Festivo(self.fecha, self.En_Linea):
            return True

       # Consultar vehículos excluidos de la restricción según la segunda letra de la placa o si se utilizan sólo dos letras
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

        # Verifique si el tiempo proporcionado no está en las horas pico prohibidas
        if not self._Es_Hora_Pico(self.hora):
            return True

        day = self.__Buscar_dia(self.fecha)  # Encuentra el día de la semana a partir de la fecha
        # Verifique si el último dígito de la placa no está restringido en este día en particular
        if int(self.placa[-1]) not in self.__restriciones[day]:
            return True

        return False
        if __name__ == '__main__':

            parser = argparse.ArgumentParser(
            description='Pico y Placa Quito Predictor: Consulta si el vehículo con la placa proporcionada puede estar en la vía en la fecha y hora indicada')
            parser.add_argument(
                '-o',
                '--EN_Linea',
                action='store_true',
                help='usar la API de días festivos de resumen')
            parser.add_argument(
                '-p',
                '--placa',
                required=True,
                help='la placa del vehículo: XXX-YYYY o XX-YYYY, donde X es una letra mayúscula e Y es un dígito')
            parser.add_argument(
                '-d',
                '--fecha',
                required=True,
                help='la fecha a comprobar: AAAA-MM-DD')
            parser.add_argument(
                '-t',
                '--hora',
                required=True,
                help='la hora a comprobar: HH:MM')
            args = parser.parse_args()
        pyp = PicoPlaca(args.placa, args.fecha, args.hora, args.En_Linea)

        if pyp.predecir():
            print(
                'El vehículo con placa {} PUEDE estar en la carretera el {} a las {}.'.format(
                    args.placa,
                    args.fecha,
                    args.hora))
        else:
            print(
                'El vehículo con placa {} NO PUEDE estar en la carretera en {} a las {}.'.format(
                    args.placa,
                    args.fecha,
                    args.hora))
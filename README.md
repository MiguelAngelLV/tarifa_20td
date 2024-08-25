# Tarifa 2.0 TD

Componente para Home Assistant para crear un sensor con el precio actual para usuarios con tarifas 2.0 TD (tres periodos) y 3.0 TD (seis periodos).

Permite saber en cada momento el precio del kWh según si es valle, llana o punta, teniendo en cuenta que los festivos y fines de semana siempre es valle.

Además crea un sensor que calcula los costes fijos diarios (potencia, alquiler de contador, bono social...).

## Instalación

### Directa usando _My Home Assistant_
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=miguelangellv&repository=tarifa_20td&category=integration)

## Manual
Puedes instalar el componente usando HACS, para ello basta con añadir este repositorio a los repositorios personalizados y buscarlo escribiendo «Tarifa».

## Configuración

Una vez instalado, ve a _Dispositivos y Servicios -> Añadir Integración_ y busca _Tarifa_.

El asistente primero te solicitará elegir la tarifa correspondiente: 2.0 o 3.0.

Lo habitual será la 2.0 TD que es la doméstica con 3 periodos.

En el siguiente paso, deberemos indicar el coste diario y los precios de cada uno de los periodos.

El coste fijo por día se refiere a costes fijos no dependientes del consumo. Normalmente este coste suele incluir potencia, bono social y alguna cuota. Lo más fácil es buscar
la última factura y dividir estos costes fijos por el número de días e introducir el resultado.

## Uso

Una vez configurado el componente, en el panel de energía añade tu sensor de energía consumida total e indica que quieres realizar el control de costes usando una entidad con el
precio actual seleccionado _Precio kWh_ como entidad.

Así mismo, puedes añadir una nueva línea de consumo con el sensor _Costes fijos_ (que siempre valdrá 0) y en sus costes configurar _Usar una entidad que realiza un seguimiento de
los costes totales_ seleccionando _Costes Fijos Totales_, de esta forma cada día añadirá el coste fijo y así tener una idea más cercana del precio final.

Además, el sensor `sensor.precio_kWh` dispone del atributo «Period» con el periodo actual (P1 = punta, P2 = llana, P3 = valle para el caso de 2.0, o de P1 a P6 para 3.0),
que puede utilizarse para automatizaciones.

## Videotutorial
[![Videotutorial](https://img.youtube.com/vi/BdZdz-7Du_Q/0.jpg)](https://www.youtube.com/watch?v=BdZdz-7Du_Q "Videotutorial")

## Balance Neto

Si tienes instalación fotovoltaica es posible que te interese mi otro componente [Balance Neto Horario](https://github.com/MiguelAngelLV/balance_neto) para calcular de forma más precia los euros.

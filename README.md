# Tarifa 2.0 TD

Componente para Home Assistant para crear un sensor con el precio actual para usuarios con tarifa de tres tramos con precios fijos.

Permite saber en cada momento el precio del kWh según si es valle, llana o punta, teniendo en cuenta que los festivos y fines de semana siempre es valle.

Además crea un sensor que calcula los costes fijos diarios (potencia, alquiler de contador, bono social...).

## Instalación
Puedes instalar el componente usando HACS, para ello basta con añadir este repositorio a los repositorios personalizados y buscarlo escribiendo «Tarifa».

## Configuración

Una vez instalado, ve a _Dispositivos y Servicios -> Añadir Integración_ y busca _Tarifa_.

El asistente te solicitará 4 precios. Los tres primeros son los precios por kWh de tu tarifa.

El cuarto es el coste fijo por día. Normalmente este coste suele incluir potencia, bono social y alguna cuota. Lo más fácil es buscar la última factura y dividir estos costes fijos por el número de días.


## Uso
Una vez configurado el componente, en el panel de energía añade tu sensor de energía consumida total e indica que quieres realizar el control de costes usando una entidad con el precio actual seleccionado _Precio kWh_ como entidad.

Así mismo, puedes añadir una nueva línea de consumo con el sensor _Costes fijos_ (que siempre valdrá 0) y en sus costes configurar _Usar una entidad que realiza un seguimiento de los costes totales_ seleccionando _Costes Fijos Totales_, de esta forma cada día añadirá el coste fijo y así tener una idea más cercana del precio final.



## Futuras ideas

Aunque actualmente está muy bajo y apenas supone diferencia, si el coste del mecanismo del gas volviese a subir, me gustaría añadir la opción de incrementar los costes añadiendo a la precio del momento el MAG asociado.


## Balance Neto

Si tienes instalación fotovoltaica es posible que te interese mi otro componente [Balance Neto Horario](https://github.com/MiguelAngelLV/balance_neto) para calcular de forma más precia los euros.

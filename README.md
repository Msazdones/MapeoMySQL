**********************************************************************************************************************************

[*]Este código ha sido desarrollado por Miguel Saz Dones, estudiante de la Universidad de Alcalá de henares (UAH), a fecha 24/02/2022, 
con la única finalidad de servir de manera didáctica al autor para entender el funcionamiento y el proceso 
de creación de una herramienta de estas características, además de comprender en mayor medida el funcionamiento 
de una base de datos SQL.

[*]Para el desarrollo de esta herramienta, se ha utilizado un como objetivo un formulario concreto y una base de datos MySQL, por lo que es 
posible que tenga que ser editado si se desea adaptarlo a otros entornos.

[*]Renuncia de responsabilidad: El autor no se hace responsable de las actividades ilegales que puedan ser perpetradas por 
otras personas empleando para ello la herramienta esta herramienta.

**********************************************************************************************************************************

[*]This script has been developed by Miguel Saz Dones, student of the University of Alcalá de Henares (UAH), on date 24/02/2022, 
with the sole purpose of serving didacticaly to the author for understanding the operation and the process of 
creating a tool of these characteristics, in addition to better understanding the operation of a SQL database.

[*]For the development of these tool, a specific web form and a MySQL database have been used as the target, so it may have to be edited if you want 
to adapt it to other environments.

[*]Disclaimer: The author accepts no responsibility for the illegal activities that may be perpetrated by other people using this tool.

**********************************************************************************************************************************

[*]Tool Execution:

        [-] python3 MapeoMySQL.py -<option> <URL>

[*]Tool Options:

        [-] h: Show help page.

        [-] d: Extract database names from given URL.

        [-] t: Extract table names from given URL and database name.

        [-] c: Extract column names from given URL, database name and table name.

        [-] i: Extract column content from given URL, database name, table name and list of columns.

[*]Example:

        [-] python3 MapeoMySQL.py -d http://127.0.0.1/webpage.html

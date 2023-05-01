PRAGMA foreign_keys = OFF;
CREATE TABLE "ventas_new" ( id_ventas INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, cantidadVent INTEGER, pUnidadVent FLOAT NOT NULL, pUnidadVent DATE, prodIdVent INTEGER, clieIdVent INTEGER,provIdVent INTEGER, FOREIGN KEY(prodIdVent) REFERENCES producto (id_producto),FOREIGN KEY(provIdVent) REFERENCES proveedor (id_proveedor), FOREIGN KEY(clieIdVent) REFERENCES cliente (id_cliente));

DROP TABLE ventas;
ALTER TABLE ventas_new RENAME TO ventas;
PRAGMA foreign_keys = ON;


CREATE TABLE "ventas" ( id_ventas INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, cantidadVent INTEGER, pUnidadVent FLOAT NOT NULL, fechaVent DATE, prodIdVent INTEGER, clieIdVent INTEGER, FOREIGN KEY(prodIdVent) REFERENCES producto (id_producto), FOREIGN KEY(clieIdVent) REFERENCES cliente (id_cliente));
INSERT INTO "main"."ventas" VALUES('2','1','12.0','12/04/2023','6','2','11');
INSERT INTO "main"."ventas" VALUES('3','1','10.0','12/04/2023','11','2','11');
INSERT INTO "main"."ventas" VALUES('4','1','11.0','01/04/2023','11','2','11');

import os
import sqlite3
import string

import flask

app = flask.Flask(__name__)

homepage: string.Template = string.Template("""
<!doctype HTML>
<head>
    <style>
        body {
            background-color: #181818;
        }
    </style>
    <title>CSV Parser</title>
</head>
<body>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
</body>
""")


def db_exists() -> bool:
    return os.path.isfile("db.db")


def setup_db():
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    # TODO
    cur.execute("""
        CREATE TABLE antenna(
            id INTEGER NOT NULL UNIQUE,
            NGR	TEXT,
            Longitude/Latitude TEXT,
            Site_Height INTEGER DEFAULT 0,
            In-Use_Ae_Ht INTEGER DEFAULT 0,
            In-Use_ERP_Total INTEGER DEFAULT 0,
            Dir_Max_ERP	INTEGER DEFAULT 0,
            0	REAL DEFAULT 0.0,
            10	REAL DEFAULT 0.0,
            20	REAL DEFAULT 0.0,
            30	REAL DEFAULT 0.0,
            40	REAL DEFAULT 0.0,
            50	REAL DEFAULT 0.0,
            60	REAL DEFAULT 0.0,
            70	REAL DEFAULT 0.0,
            80	REAL DEFAULT 0.0,
            90	REAL DEFAULT 0.0,
            100	REAL DEFAULT 0.0,
            110	REAL DEFAULT 0.0,
            120	REAL DEFAULT 0.0,
            130	REAL DEFAULT 0.0,
            140	REAL DEFAULT 0.0,
            150	REAL DEFAULT 0.0,
            160	REAL DEFAULT 0.0,
            170	REAL DEFAULT 0.0,
            180	REAL DEFAULT 0.0,
            190	REAL DEFAULT 0.0,
            200	REAL DEFAULT 0.0,
            210	REAL DEFAULT 0.0,
            220	REAL DEFAULT 0.0,
            230	REAL DEFAULT 0.0,
            240	REAL DEFAULT 0.0,
            250	REAL DEFAULT 0.0,
            260	REAL DEFAULT 0.0,
            270	REAL DEFAULT 0.0,
            280	REAL DEFAULT 0.0,
            290	REAL DEFAULT 0.0,
            300	REAL DEFAULT 0.0,
            310	REAL DEFAULT 0.0,
            320	REAL DEFAULT 0.0,
            330	REAL DEFAULT 0.0,
            340	REAL DEFAULT 0.0,
            350	REAL DEFAULT 0.0,
            Lat	REAL DEFAULT 0.0,
            Long REAL DEFAULT 0.0,
        );
    """)

    cur.execute("""
        CREATE TABLE params(
            id INTEGER NOT NULL UNIQUE,
            Date TEXT,
            Ensemble TEXT,
            Licence TEXT,
            Ensemble_Area TEXT,
            EID	TEXT,
            Transmitter_Area TEXT,
            Site TEXT,
            Freq. REAL DEFAULT 0.0, TEXT,
            Block TEXT,
            TII_Main_Id_(Hex) TEXT,
            TII_Sub_Id_(Hex) TEXT,
            Serv_Label1  TEXT,
            SId_1 (Hex) TEXT,
            LSN_1 (Hex) TEXT,
            Serv_Label2  TEXT,
            SId_2 (Hex) TEXT,
            LSN_2 (Hex) TEXT,
            Serv_Label3  TEXT,
            SId_3 (Hex) TEXT,
            LSN_3 (Hex) TEXT,
            Serv_Label4  TEXT,
            SId_4 (Hex) TEXT,
            LSN_4 (Hex) TEXT,
            Serv_Label5 TEXT,
            SId_5 (Hex) TEXT,
            LSN_5 (Hex) TEXT,
            Serv_Label6  TEXT,
            SId_6 (Hex) TEXT,
            LSN_6 (Hex) TEXT,
            Serv_Label7  TEXT,
            SId_7 (Hex) TEXT,
            LSN_7 (Hex) TEXT,
            Serv_Label8  TEXT,
            SId_8 (Hex) TEXT,
            LSN_8 (Hex) TEXT,
            Serv_Label9  TEXT,
            SId_9 (Hex) TEXT,
            LSN_9 (Hex) TEXT,
            Serv_Label10  TEXT,
            SId_10_(Hex) TEXT,
            LSN_10_(Hex) TEXT,
            Serv_Label11  TEXT,
            SId_11_(Hex) TEXT,
            LSN_11_(Hex) TEXT,
            Serv_Label12  TEXT,
            SId_12_(Hex) TEXT,
            LSN_12_(Hex) TEXT,
            Serv_Label13  TEXT,
            SId_13_(Hex) TEXT,
            LSN_13_(Hex) TEXT,
            Serv_Label14 TEXT,
            SId_14_(Hex) TEXT,
            LSN_14_(Hex) TEXT,
            Serv_Label15 TEXT,
            SId_15_(Hex) TEXT,
            LSN_15_(Hex) TEXT,
            Serv_Label16  TEXT,
            SId_16_(Hex) TEXT,
            LSN_16_(Hex) TEXT,
            Serv_Label17  TEXT,
            SId_17_(Hex) TEXT,
            LSN_17_(Hex) TEXT,
            Serv_Label18  TEXT,
            SId_18_(Hex) TEXT,
            LSN_18_(Hex) TEXT,
            Serv_Label19  TEXT,
            SId_19_(Hex) TEXT,
            LSN_19_(Hex) TEXT,
            Serv_Label20  TEXT,
            SId_20_(Hex) TEXT,
            LSN_20_(Hex) TEXT,
            Serv_Label21  TEXT,
            SId_21_(Hex) TEXT,
            LSN_21_(Hex) TEXT,
            Serv_Label22  TEXT,
            SId_22_(Hex) TEXT,
            LSN_22_(Hex) TEXT,
            Serv_Label23  TEXT,
            SId_23_(Hex) TEXT,
            LSN_23_(Hex) TEXT,
            Serv_Label24  TEXT,
            SId_24_(Hex) TEXT,
            LSN_24_(Hex) TEXT,
            Serv_Label25  TEXT,
            SId_25_(Hex) TEXT,
            LSN_25_(Hex) TEXT,
            Serv_Label26  TEXT,
            SId_26_(Hex) TEXT,
            LSN_26_(Hex) TEXT,
            Serv_Label27  TEXT,
            SId_27_(Hex) TEXT,
            LSN_27_(Hex) TEXT,
            Serv_Label28  TEXT,
            SId_28_(Hex) TEXT,
            LSN_28_(Hex) TEXT,
            Serv_Label29  TEXT,
            SId_29_(Hex) TEXT,
            LSN_29_(Hex) TEXT,
            Serv_Label30  TEXT,
            SId_30_(Hex) TEXT,
            LSN_30_(Hex) TEXT,
            Serv_Label31  TEXT,
            SId_31_(Hex) TEXT,
            LSN_31_(Hex) TEXT,
            Serv_Label32  TEXT,
            SId_32_(Hex) TEXT,
            LSN_32_(Hex) TEXT,
            Data_Serv_Label1 TEXT,
            Data_SId_1 (Hex) TEXT,
            Data_Serv_Label2 TEXT,
            Data_SId_2 (Hex) TEXT,
            Data_Serv_Label3 TEXT,
            Data_SId_3 (Hex) TEXT,
            Data_Serv_Label4 TEXT,
            Data_SId_4 (Hex) TEXT,
            Data_Serv_Label5 TEXT,
            Data_SId_5 (Hex) TEXT,
            Data_Serv_Label6 TEXT,
            Data_SId_6 (Hex) TEXT,
            Data_Serv_Label7 TEXT,
            Data_SId_7 (Hex) TEXT,
            Data_Serv_Label8 TEXT,
            Data_SId_8 (Hex) TEXT,
            Data_Serv_Label9 TEXT,
            Data_SId_9 (Hex) TEXT,
            Data_Serv_Label10 TEXT,
            Data_SId_10_(Hex) TEXT,
            Data_Serv_Label11 TEXT,
            Data_SId_11_(Hex) TEXT,
            Data_Serv_Label12 TEXT,
            Data_SId_12_(Hex) TEXT,
            Data_Serv_Label13 TEXT,
            Data_SId_13_(Hex) TEXT,
            Data_Serv_Label14 TEXT,
            Data_SId_14_(Hex) TEXT,
            Data_Serv_Label15 TEXT,
            Data_SId_15_(Hex) TEXT,
        );
    """)


def parse_file(text: list[str], filename: str):
    if not text:
        return
    headers = text[0]

    for line in text[1:]:
        ...


@app.route("/antenna")
def antenna():
    ...


@app.route("/params")
def params():
    ...


@app.route("/", methods=["GET", "POST"])
def index():
    if not db_exists():
        setup_db()

    if flask.request.method == "POST":
        f = flask.request.files["file"]
        text = [line.decode("utf-8") for line in f]
        parse_file(text, f.filename)
        return "<p>thx</p>"
    else:
        return homepage.substitute()


import csv
import os
import sqlite3
import tkinter
from tkinter import filedialog
from tkinter import ttk
from typing import Callable

ANTENNAS_HEADERS: list[str] = [
    "id", "NGR", "LongitudeLatitude", "Site_Height", "In", "In",
    "Dir_Max_ERP", "0", "10", "20", "30", "40", "50", "60", "70",
    "80", "90", "100", "110", "120", "130", "140", "150", "160",
    "170", "180", "190", "200", "210", "220", "230", "240", "250",
    "260", "270", "280", "290", "300", "310", "320", "330", "340",
    "350", "Lat", "Long",
]
PARAMS_HEADERS: list[str] = [
    "id", "Date", "Ensemble", "Licence", "Ensemble_Area", "EID" "Transmitter_Area",
    "Site", "Freq" "Block", "TII_Main_Id_(Hex)", "TII_Sub_Id_(Hex)", "Serv_Label1",
    "SId_1_(Hex)", "LSN_1_(Hex)", "Serv_Label2", "SId_2_(Hex)", "LSN_2_(Hex)",
    "Serv_Label3", "SId_3_(Hex)", "LSN_3_(Hex)", "Serv_Label4", "SId_4_(Hex)",
    "LSN_4_(Hex)", "Serv_Label5", "SId_5_(Hex)", "LSN_5_(Hex)", "Serv_Label6",
    "SId_6_(Hex)", "LSN_6_(Hex)", "Serv_Label7", "SId_7_(Hex)", "LSN_7_(Hex)",
    "Serv_Label8", "SId_8_(Hex)", "LSN_8_(Hex)", "Serv_Label9", "SId_9_(Hex)",
    "LSN_9_(Hex)", "Serv_Label10", "SId_10_(Hex)", "LSN_10_(Hex)", "Serv_Label11",
    "SId_11_(Hex)", "LSN_11_(Hex)", "Serv_Label12", "SId_12_(Hex)", "LSN_12_(Hex)",
    "Serv_Label13", "SId_13_(Hex)", "LSN_13_(Hex)", "Serv_Label14", "SId_14_(Hex)",
    "LSN_14_(Hex)", "Serv_Label15", "SId_15_(Hex)", "LSN_15_(Hex)", "Serv_Label16",
    "SId_16_(Hex)", "LSN_16_(Hex)", "Serv_Label17", "SId_17_(Hex)", "LSN_17_(Hex)",
    "Serv_Label18", "SId_18_(Hex)", "LSN_18_(Hex)", "Serv_Label19", "SId_19_(Hex)",
    "LSN_19_(Hex)", "Serv_Label20", "SId_20_(Hex)", "LSN_20_(Hex)", "Serv_Label21",
    "SId_21_(Hex)", "LSN_21_(Hex)", "Serv_Label22", "SId_22_(Hex)", "LSN_22_(Hex)",
    "Serv_Label23", "SId_23_(Hex)", "LSN_23_(Hex)", "Serv_Label24", "SId_24_(Hex)",
    "LSN_24_(Hex)", "Serv_Label25", "SId_25_(Hex)", "LSN_25_(Hex)", "Serv_Label26",
    "SId_26_(Hex)", "LSN_26_(Hex)", "Serv_Label27", "SId_27_(Hex)", "LSN_27_(Hex)",
    "Serv_Label28", "SId_28_(Hex)", "LSN_28_(Hex)", "Serv_Label29", "SId_29_(Hex)",
    "LSN_29_(Hex)", "Serv_Label30", "SId_30_(Hex)", "LSN_30_(Hex)", "Serv_Label31",
    "SId_31_(Hex)", "LSN_31_(Hex)", "Serv_Label32", "SId_32_(Hex)", "LSN_32_(Hex)",
    "Data_Serv_Label1", "Data_SId_1_(Hex)", "Data_Serv_Label2", "Data_SId_2_(Hex)",
    "Data_Serv_Label3", "Data_SId_3_(Hex)", "Data_Serv_Label4", "Data_SId_4_(Hex)",
    "Data_Serv_Label5", "Data_SId_5_(Hex)", "Data_Serv_Label6", "Data_SId_6_(Hex)",
    "Data_Serv_Label7", "Data_SId_7_(Hex)", "Data_Serv_Label8", "Data_SId_8_(Hex)",
    "Data_Serv_Label9", "Data_SId_9_(Hex)", "Data_Serv_Label10", "Data_SId_10_(Hex)",
    "Data_Serv_Label11", "Data_SId_11_(Hex)", "Data_Serv_Label12", "Data_SId_12_(Hex)",
    "Data_Serv_Label13", "Data_SId_13_(Hex)", "Data_Serv_Label14", "Data_SId_14_(Hex)",
    "Data_Serv_Label15", "Data_SId_15_(Hex)",
]


def db_exists() -> bool:
    return os.path.isfile("db.db")


def setup_db() -> None:
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS antenna(
            id INTEGER NOT NULL UNIQUE,
            NGR    TEXT,
            LongitudeLatitude TEXT,
            Site_Height INTEGER DEFAULT 0,
            In_Use_Ae_Ht INTEGER DEFAULT 0,
            In_Use_ERP_Total INTEGER DEFAULT 0,
            Dir_Max_ERP    INTEGER DEFAULT 0,
            '0'    REAL DEFAULT 0.0, '10' REAL DEFAULT 0.0, '20' REAL DEFAULT 0.0,
            '30'    REAL DEFAULT 0.0, '4' REAL DEFAULT 0.0, '50' REAL DEFAULT 0.0,
            '60'    REAL DEFAULT 0.0, '70' REAL DEFAULT 0.0, '80' REAL DEFAULT 0.0,
            '90'    REAL DEFAULT 0.0, '100' REAL DEFAULT 0.0, '110'    REAL DEFAULT 0.0,
            '120'    REAL DEFAULT 0.0, '130' REAL DEFAULT 0.0, '140'    REAL DEFAULT 0.0,
            '150'    REAL DEFAULT 0.0, '160' REAL DEFAULT 0.0, '170'    REAL DEFAULT 0.0,
            '180'    REAL DEFAULT 0.0, '190' REAL DEFAULT 0.0, '200'    REAL DEFAULT 0.0,
            '210'    REAL DEFAULT 0.0, '220' REAL DEFAULT 0.0, '230'    REAL DEFAULT 0.0,
            '240'    REAL DEFAULT 0.0, '250' REAL DEFAULT 0.0, '260'    REAL DEFAULT 0.0,
            '270'    REAL DEFAULT 0.0, '280' REAL DEFAULT 0.0, '290'    REAL DEFAULT 0.0,
            '300'    REAL DEFAULT 0.0, '310' REAL DEFAULT 0.0, '320'    REAL DEFAULT 0.0,
            '330'    REAL DEFAULT 0.0, '340' REAL DEFAULT 0.0, '350'    REAL DEFAULT 0.0,
            Lat    REAL DEFAULT 0.0, Long REAL DEFAULT 0.0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS params(
            id INTEGER NOT NULL UNIQUE,
            Date TEXT,
            Ensemble TEXT,
            Licence TEXT,
            Ensemble_Area TEXT,
            EID    TEXT,
            Transmitter_Area TEXT,
            Site TEXT,
            Freq REAL DEFAULT 0.0,
            Block TEXT,
            TII_Main_Id TEXT,
            TII_Sub_Id TEXT,
            Serv_Label1  TEXT, SId_1 TEXT, LSN_1 TEXT, Serv_Label2  TEXT,
            SId_2 TEXT, LSN_2 TEXT, Serv_Label3  TEXT, SId_3 TEXT,
            LSN_3 TEXT, Serv_Label4  TEXT, SId_4 TEXT, LSN_4 TEXT,
            Serv_Label5 TEXT, SId_5 TEXT, LSN_5 TEXT, Serv_Label6  TEXT,
            SId_6 TEXT, LSN_6 TEXT, Serv_Label7  TEXT, SId_7 TEXT,
            LSN_7 TEXT, Serv_Label8  TEXT, SId_8 TEXT, LSN_8 TEXT,
            Serv_Label9  TEXT, SId_9 TEXT, LSN_9 TEXT, Serv_Label10  TEXT,
            SId_10 TEXT, LSN_10 TEXT, Serv_Label11  TEXT, SId_11 TEXT,
            LSN_11 TEXT, Serv_Label12  TEXT, SId_12 TEXT, LSN_12 TEXT,
            Serv_Label13  TEXT, SId_13 TEXT, LSN_13 TEXT, Serv_Label14 TEXT,
            SId_14 TEXT, LSN_14 TEXT, Serv_Label15 TEXT, SId_15 TEXT,
            LSN_15 TEXT, Serv_Label16  TEXT, SId_16 TEXT, LSN_16 TEXT,
            Serv_Label17  TEXT, SId_17 TEXT, LSN_17 TEXT, Serv_Label18  TEXT,
            SId_18 TEXT, LSN_18 TEXT, Serv_Label19  TEXT, SId_19 TEXT,
            LSN_19 TEXT, Serv_Label20  TEXT, SId_20 TEXT, LSN_20 TEXT,
            Serv_Label21  TEXT, SId_21 TEXT, LSN_21 TEXT, Serv_Label22  TEXT,
            SId_22 TEXT, LSN_22 TEXT, Serv_Label23  TEXT, SId_23 TEXT,
            LSN_23 TEXT, Serv_Label24  TEXT, SId_24 TEXT, LSN_24 TEXT,
            Serv_Label25  TEXT, SId_25 TEXT, LSN_25 TEXT, Serv_Label26  TEXT,
            SId_26 TEXT, LSN_26 TEXT, Serv_Label27  TEXT, SId_27 TEXT,
            LSN_27 TEXT, Serv_Label28  TEXT, SId_28 TEXT, LSN_28 TEXT,
            Serv_Label29  TEXT, SId_29 TEXT, LSN_29 TEXT, Serv_Label30  TEXT,
            SId_30 TEXT, LSN_30 TEXT, Serv_Label31  TEXT, SId_31 TEXT,
            LSN_31 TEXT, Serv_Label32  TEXT, SId_32 TEXT, LSN_32 TEXT,
            Data_Serv_Label1 TEXT, Data_SId_1 TEXT, Data_Serv_Label2 TEXT,
            Data_SId_2 TEXT, Data_Serv_Label3 TEXT, Data_SId_3 TEXT,
            Data_Serv_Label4 TEXT, Data_SId_4 TEXT, Data_Serv_Label5 TEXT,
            Data_SId_5 TEXT, Data_Serv_Label6 TEXT, Data_SId_6 TEXT,
            Data_Serv_Label7 TEXT, Data_SId_7 TEXT, Data_Serv_Label8 TEXT,
            Data_SId_8 TEXT, Data_Serv_Label9 TEXT, Data_SId_9 TEXT,
            Data_Serv_Label10 TEXT, Data_SId_10 TEXT, Data_Serv_Label11 TEXT,
            Data_SId_11 TEXT, Data_Serv_Label12 TEXT, Data_SId_12 TEXT,
            Data_Serv_Label13 TEXT, Data_SId_13 TEXT, Data_Serv_Label14 TEXT,
            Data_SId_14 TEXT, Data_Serv_Label15 TEXT, Data_SId_15 TEXT
        );
    """)

    conn.commit()
    conn.close()


def get_params_table() -> list[list[str]]:
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM params;")
    return res.fetchall()


def get_antennas_table() -> list[list[str]]:
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM antenna;")
    return res.fetchall()


def parse_file(filename: str) -> None:
    try:
        with open(filename) as f:
            lines = list(csv.reader(f, delimiter=',', quotechar='"'))
    except UnicodeDecodeError:
        tkinter.messagebox.showerror(
            "Invalid",
            "Invalid file encoding uploaded. Provided file is not utf-8 compliant."
        )

        return;

    conn = sqlite3.connect("db.db")
    cur = conn.cursor()

    headers = lines[0]

    if headers[1] == ANTENNAS_HEADERS[1]:
        cur.executemany(
            f"INSERT INTO antenna VALUES({'?,' * (len(headers) - 1)} ?);",
            lines[1:]
        )

    elif headers[1] == PARAMS_HEADERS[1]:
        cur.executemany(
            f"INSERT INTO params VALUES({'?,' * (len(headers) - 1)} ?);",
            lines[1:]
        )

    conn.commit()
    conn.close()


def upload_file() -> None:
    file_path = filedialog.askopenfilename()
    if file_path:
        parse_file(file_path)


def build_table(
    frame: ttk.Frame,
    cols: list[str],
    query_func: Callable[[], list[list[str]]]
) -> ttk.Treeview:
    table = ttk.Treeview(frame)
    table["columns"] = cols
    table.tag_configure('oddrow', background='#E8E8E8')
    table.tag_configure('evenrow', background='#FFFFFF')

    table.column('#0', width=0, stretch=tkinter.NO)
    table.heading('#0', text='', anchor=tkinter.W)

    for col in cols:
        table.column(col, anchor=tkinter.W, width=150)
        table.heading(col, text=col, anchor=tkinter.W)

    for idx, row in enumerate(query_func()):
        table.insert(
            parent='',
            index=1,
            values=row,
            tags=("oddrow") if idx % 2 else ("evenrow")
        )

    table.pack(expand=True, fill=tkinter.BOTH)
    return table


def main() -> int:
    if not db_exists():
        setup_db()

    selected_table = ""
    entries = []

    def submit_changes():
        nonlocal selected_table
        nonlocal entries

        headers = ANTENNAS_HEADERS if selected_table == "antenna" else PARAMS_HEADERS
        values = [e.get() for e in entries]
        set_vals = ""
        for header, value in list(zip(headers[1:], values[1:])):
            set_vals += f"{header} = \"{value}\""
            if header != headers[-1]:
                set_vals += ", "

        conn = sqlite3.connect("db.db")
        cur = conn.cursor()
        res = cur.execute(f"UPDATE {selected_table} SET {set_vals} WHERE id = {values[0]};")

        conn.commit()
        conn.close()

    def modify_row() -> None:
        nonlocal lhs_tbl
        nonlocal rhs_tbl
        nonlocal selected_table
        nonlocal entries

        popup = tkinter.Toplevel(win)
        popup.title("Modify row")

        # Stores the index of the selected row
        selected_row = lhs_tbl.focus()
        values = lhs_tbl.item(selected_row, "values")
        headers = ANTENNAS_HEADERS
        selected_table = "antenna"
        if values is None:
            selected_row = rhs_tbl.focus()
            values = rhs_tbl.item(selected_row, "values")
            headers = PARAMS_HEADERS
            selected_table = "params"

        header_val_pairs = list(zip(headers, values))
        for idx, val in enumerate(header_val_pairs):
            tkinter.Label(popup, text=val[0]).grid(row=idx, column=0)
            entry = tkinter.Entry(popup)
            entry.grid(row=idx, column=1)
            entry.insert(0, val[1])
            entries.append(entry)

        tkinter.Button(popup, text="Submit Changes", command=submit_changes).grid(sticky="NSEW")

    win = tkinter.Tk()
    win.title("Window")
    win.geometry("980x540")

    lhs_frame = ttk.Frame(win, borderwidth=1)
    lhs_frame.place(relx=0.05, rely=0.01, relwidth=0.4, relheight=0.75)
    lhs_tbl = build_table(lhs_frame, ANTENNAS_HEADERS, get_antennas_table)

    rhs_frame = ttk.Frame(win, borderwidth=1)
    rhs_frame.place(relx = 0.55, rely=0.01, relwidth=0.4, relheight=0.75)
    rhs_tbl = build_table(rhs_frame, PARAMS_HEADERS, get_params_table)

    upload_btn = tkinter.Button(win, text="Upload File", command=upload_file)
    upload_btn.place(relx=0.2, rely=0.8)
    modify_btn = tkinter.Button(win, text="Modify", command=modify_row)
    modify_btn.place(relx=0.75, rely=0.8)

    win.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

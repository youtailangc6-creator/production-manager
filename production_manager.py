from datetime import date

print("Production Manager Ver.") 

def show_menu():
    print()
    print("="*38)
    print(".    Production Manager")
    print("="*38)

    print("1. 生産実績を追加")
    print("2. 実績一覧を見る")
    print("3. 製品別に集計")
    print("4. 不良率を確認")
    print("5. 記録を修正")
    print("6. 記録を削除")
    print("7. 終了")
    print("="*38)

def add_production_record():
    print("===== 生産実績追加 =====")
    today=date.today()
    product_name=input("製品名を入力してください")
    production_count=int(input("生産数を入力してください"))
    defect_count=int(input("不良数を入力してください"))
    defective_rate=defect_count/production_count*100
    defective_rate=round(defective_rate,2)

    record=f"{today},{product_name},{production_count},{defect_count},{defective_rate}"

    with open("production_history.csv","a")as file:
        file.write(record+"\n")

    print("生産実績を保存しました")
    print("保存内容:",record) 

def show_production_records():
    print("===== 生産実績一覧 =====")
    
    with open("production_history.csv","r")as file:
         for line in file:
              print(line.strip())

def production_summary():
    summary={}
    with open("production_history.csv","r")as file:
        for line in file:
            date=line.split(",")
            production_name=date[1]
            production_number=int(date[2])

            if production_name in summary:
                 summary[production_name]=summary[production_name]+production_number
            else:
                summary[production_name]=production_number

    for  production_name,total in summary.items():
         print(f"{production_name}:{total}個")

def defect_summary():
    production_summary={}
    defect_summary={}
    with open("production_history.csv","r")as file:
        for line in file:
            record=line.split(",")
            production_name=record[1]
            production_number=int(record[2])
            defect_number=int(record[3])

            if production_name in production_summary:
               production_summary[production_name]=production_summary[production_name]+production_number
            else:
                production_summary[production_name]=production_number

            if production_name in defect_summary:
                defect_summary[production_name]=defect_summary[production_name]+defect_number
            else:
                defect_summary[production_name]=defect_number

    print("===== 不良率一覧 =====")
    for production_name,production_total in production_summary.items():
        defect_total=defect_summary[production_name]
        defect_rate=defect_total/production_total*100
        defect_rate=round(defect_rate,2)
        print(f"{production_name}:{defect_rate}%")

def edit_production_record():
    records=[]

    with open("production_history.csv","r")as file:
        for line in file:
            records.append(line.strip())
        for number,date in enumerate(records,start=1):
            parts=date.split(",")
        print(f"{number:},{parts[0]},{parts[1]},{parts[2]}個 不良{parts[3]}個")   

    try:    
       edit_number=int(input("修正する番号を入力してください"))
    except ValueError:
        print("数字を入力してください")
        return    
    edit_index=edit_number-1
    if edit_number < 1 or edit_number > len(records):
       print("存在する番号を入力してください")
       return
    selected_record=records[edit_index]
    print(selected_record)

    selected_parts=selected_record.split(",")

    print("1. 製品名")
    print("2. 生産数")
    print("3. 不良数")

    edit_item=input("修正する項目は？")

    if edit_item=="1":
        new_name=input("新しい製品名:？")
        selected_parts[1]=new_name
    elif edit_item=="2":
        new_production=input("生産数:")
        selected_parts[2]=new_production
    elif edit_item=="3":
        new_defect=input("新しい不良数:")
        selected_parts[3]=new_defect   

    new_record=",".join(selected_parts) 
    records[edit_index]=new_record  

    for new_record in records:
        print(new_record)

    with open("production_history.csv","w")as file:
        for record in records:
            file.write(record+"\n")

def delete_production_record():
    records=[]
    with open("production_history.csv","r")as file:
        for line in file:
            records.append(line.strip())

        for number,record in enumerate(records,start=1):
            parts=record.split(",")
            today=parts[0]
            production_name=parts[1]
            production_number=parts[2]
            defect_number=parts[3]
            print(f"{number},{today},{production_name},{production_number},{defect_number}")  
    try:
        delete_number=int(input("削除したい番号を入力してください"))
    except ValueError:
        print("数字を入力してください")
        return

    delete_index=delete_number-1
    if delete_number < 1 or delete_number > len(records):
       print("存在する番号を入力してください")
       return  

    confirm=input("本当に削除しますか？(y/n):")
    if confirm=="y":
        records.pop(delete_index)

        with open("production_history.csv","w")as file:
            for record in records:
             file.write(record+"\n")

        print("記録を削除しました")

    else:
        print("キャンセルしました")


while True:
    show_menu()
    choice=input("番号を入力してください:")  

    if choice=="1":
        add_production_record()

    elif choice=="2":
        show_production_records()

    elif choice=="3":
        production_summary() 

    elif choice=="4":
        defect_summary()  

    elif choice=="5":
        edit_production_record()

    elif choice=="6":
        delete_production_record()    

    elif choice=="7":
         print("終了")
         break
    else:
        print("1~7の番号を入力してください:")           

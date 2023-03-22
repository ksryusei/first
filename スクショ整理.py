import glob
import os
import shutil
import datetime
import time
import sys
import codecs

path = glob.glob("C:/Users/ironr/OneDrive/画像/スクリーンショット/スクリーンショット *")
pathlens = len(path)
print(pathlens)
print(path)
#ファイルのパスをリスト型で取得

def d_copy_paste(from_path, to_path):
    print("d_copy_past関数実行")

    f_path = to_path
    ####保存先フォルダに同じ名前のファイルがあれば末尾に"_数字"をつける####
    f_path2 = f_path[0:f_path.rfind("\\")]
    f_name = f_path[f_path.rfind("\\") + 1:len(f_path)]
    # print(f_path2)
    # print(f_name)
    files = os.listdir(f_path2)
    # print(files)
    num = 0
    while num == 0:
        f_extension = f_name[f_name.rfind("."):len(f_name)]  ###書き込むファイルの拡張子を抽出
        name = f_name[0:f_name.rfind(".")]  ###書き込むファイル名を抽出
        count = 0  ####条件式の分岐のためにここに必要
        n_count = 1
        for i in files:
            # print(i)
            f = i[0:i.rfind(".")]
            # print(f)
            # print(name)
            if f_name == i:
                # print(n_count)
                f_name = name + "_" + str(n_count) + f_extension
                n_count = n_count + 1
            else:
                count = count + 1
        # print(count)
        # print(len(files))
        # print(f_name)
        if count == len(files):
            num = 1
    # print("wile_end")
    w_path = path.join(f_path2,f_name)
    #print(w_path)
    shutil.copyfile(from_path,w_path)



if __name__ == '__main__':
    from_path = path.join(path.dirname(__file__),"test.txt")
    to_path = path.join(path.dirname(__file__),"test_2.txt")
    a=d_copy_paste(from_path,to_path)



for p in path:
    t = os.path.getctime(p)
    d = datetime.datetime.fromtimestamp(t)
    print(d)
    print(d.strftime('%H, %M, %a'))
    print(d.weekday())
    taketm = int(d.strftime('%H'))  #撮った時間を数値として格納
    takemn = int(d.strftime('%M'))
    takedt = d.weekday()            #撮った曜日を数値として格納
    if 14 <= taketm and taketm <= 15 and takedt ==1:
        newname1 = newpath1(p)
        newname1 = p.replace('/画像/スクリーンショット/電気エネルギー工学, /画像/スクリーンショット')
        os.rename(p, newname1)
        shutil.move(newname1, "C:/Users/ironr/OneDrive/画像/スクリーンショット/電気エネルギー工学")
    elif taketm == 16 and takemn <= 19 and takedt == 1:
        newname2 = newpath1(p)
        newname2 = p.replace('/画像/スクリーンショット/電気エネルギー工学, /画像/スクリーンショット')
        os.rename(p, newname2)
        shutil.move(newname2, "C:/Users/ironr/OneDrive/画像/スクリーンショット/電気エネルギー工学")
    elif 13 <= taketm and taketm <= 15 and takedt ==2:
        newname3 = newpath2(p)
        newname3 = p.replace('/画像/スクリーンショット/電気電子工学特別講義Ⅱ, /画像/スクリーンショット')
        os.rename(p, newname3)
        shutil.move(newname3, "C:/Users/ironr/OneDrive/画像/スクリーンショット/電気電子工学特別講義Ⅱ")
    elif taketm == 16 and takemn <= 19 and takedt == 2:
        newname4 = newpath2(p)
        newname4 = p.replace('/画像/スクリーンショット/電気電子工学特別講義Ⅱ, /画像/スクリーンショット')
        os.rename(p, newname4)
        shutil.move(newname4, "C:/Users/ironr/OneDrive/画像/スクリーンショット/電気電子工学特別講義Ⅱ")
    elif taketm == 17:
        from_name = p
        to_name = "C:/Users/ironr/OneDrive/画像/スクリーンショット/電気電子工学特別講義Ⅱ"
        d_copy_paste(from_name, to_name)
    else:
        continue

print('正常に終了しました。')

time.sleep(3)

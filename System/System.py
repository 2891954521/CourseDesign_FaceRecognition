import time
import os

class System:

    '''
     ————————————————
    版权声明：本文为CSDN博主「guiruozhai」的原创文章，遵循CC
    4.0
    BY - SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https: // blog.csdn.net / qq_37989107 / article / details / 91048701
    '''

    #若重复刷脸
    def readname(self):
        
        filePath = 'C:/Users/LroSE/Desktop/Photos/照片.jpg'    #filePath为储存人脸数据的文件
        name = os.listdir(filePath)
        return name
    if __name__ == "__main__":
        name = readname()
        print("您已完成签到！")
    else:
        print("您还不是本班学生！")


    #迟到早退
    '''
    ————————————————
    版权声明：本文为CSDN博主「鱼香土豆丝」的原创文章，遵循CC
    4.0
    BY - SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https: // blog.csdn.net / he_min / article / details / 51773354
    '''

    def compare_time(time_begin, time_end):
        import time
        import datetime
        date_1 = time.strptime(time_begin, "%H:%M")
        date_2 = time.strptime(time_end, "%H:%M")

        date1 = datetime.datetime(date_1[0], date_1[1], date_1[2], date_1[3], date_1[4], date_1[5])
        date2 = datetime.datetime(date_2[0], date_2[1], date_2[2], date_2[3], date_2[4], date_2[5])
        # print date2-date1
        return date2 - date1

    def compute_time(time_begin, time_end):
        hour, minu = (int)(str(compare_time(time_begin, time_end))[0]),  \
                     (int)(str(compare_time(time_begin, time_end))[2]) * 10  \
                     + (int)(str(compare_time(time_begin, time_end))[3])
        return hour * 60 + minu



    def com_chidao(time_begin, time_s_beg):
        a = 0
        b = 0
        try:
            a = compute_time(time_begin, time_s_beg)
        except Exception:
            b = compute_time(time_s_beg, time_begin)
            return a, b

    def com_zaotui(time_begin, time_s_beg):
        c = 0
        d = 0
        try:
            c = compute_time(time_begin, time_s_beg)
        except Exception:
            d = compute_time(time_s_beg, time_begin)
            return c, d

    def judge_morning(time_list):
        time_begin = time_list[0]
        time_s_beg = u'8:00'
        time_end = time_list[1]
        time_s_end = u'12:00'
        if time_begin == '':
            print('早上没来')
        elif time_begin != '' and time_end == '':
            print('未签退')
        elif time_begin != '' and time_end != '':
            a, b = com_chidao(time_begin, time_s_beg)
            # c,d = com_zaotui(time_s_end,time_end)
            if a == 0 and b != 0:
                print('迟到%d分' % b)
            # if c==0 and d!=0:
            # print '早退%d分'%d
            else:
                print(compare_time(time_begin, time_end))

    def judge_afternoon(time_list):
        time_begin = time_list[2]
        time_s_beg = u'14:00'
        time_end = time_list[3]
        time_s_end = u'18:00'
        if time_begin == '':
            print('下午没来')
        elif time_begin != '' and time_end == '':
            print('未签退')
        elif time_begin != '' and time_end != '':
            a, b = com_chidao(time_begin, time_s_beg)
            # c,d = com_zaotui(time_s_end,time_end)
            if a == 0 and b != 0:
                print('迟到%d分' % b)
            # if c==0 and d!=0:
            # print '早退%d分'%d
            else:
                print(compare_time(time_begin, time_end))

    if __name__ == '__main__':
        chidao = 0
        kuang = 0
        kuang_day = 0
        val_time = 0
        all_time = 0
        data = []

        table = readtable()
        print('done')
        for i in range(get_num_nrow(table)):
            value = table.row_values(i)
            if value[0][3] == '日':
                continue

            time_1_be, time_1_end, time_2_be, time_2_end, time_3_be, time_3_end = value[1], value[3], value[6], value[
                8], value[10], value[12]
            # print time_1_be , time_1_end , time_2_be ,time_2_end , time_3_be , time_3_end
            time_list = [time_1_be, time_1_end, time_2_be, time_2_end, time_3_be, time_3_end]

            if time_list[0] == '旷课':
                print('旷课')
                kuang_day += 1
                kuang += 3
                continue

            # print time_list[0]
            # judje mornaing
            judge_morning(time_list)
            # judje afternoon
            judge_afternoon(time_list)
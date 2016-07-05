import sys,os,re,argparse


def getMentionList(filein,fileout,full_mention):
    uid = 0
    mid = 0
    umention_f = 0
    umention_l = 0
    mmention_f = 0
    mmention_l = 0
    u_nmentions = 0
    m_nmentions = 0
    curdir = 0
    counterl = 0

    fileout.write('userid,mentionid,firstmention_user,lastmention_user,firstmention_mentionee,lastmention_mentionee,nmentions_user,nmentions_mentionee')
    fileout.write('\n')
    for line in filein:
        l = line.strip().split(',')
        uid_c = int(l[0])
        mid_c = int(l[1])
        men_c = float(l[3])
        curdir_c = int(l[2])
        if uid == 0:
            uid = uid_c
            mid = mid_c
            curdir = curdir_c
            umention_f = men_c
            u_nmentions = 1
        else:
            if uid_c != uid or mid_c != mid:
                if ((u_nmentions * m_nmentions) > 0) or (full_mention):
                    if curdir == 0:
                        fileout.write(str(uid)+','+str(mid)+','+str(umention_f)+','+str(umention_l)+','+str(mmention_f)+','+str(mmention_l)+','+str(u_nmentions)+','+str(m_nmentions))
                        fileout.write('\n')
                    else:
                        fileout.write(str(mid)+','+str(uid)+','+str(umention_f)+','+str(umention_l)+','+str(mmention_f)+','+str(mmention_l)+','+str(u_nmentions)+','+str(m_nmentions))
                        fileout.write('\n')

                uid = uid_c
                mid = mid_c
                curdir = curdir_c
                umention_f = men_c
                umention_l = 0
                mmention_f = 0
                mmention_l = 0
                u_nmentions = 1
                m_nmentions = 0
            else:
                if curdir_c != curdir:
                    if mmention_f == 0:
                        mmention_f = men_c
                    else:
                        mmention_l = men_c
                    m_nmentions +=1
                else:
                    if umention_f == 0:
                        print("We should not have reached point ZAXOU, error")
                        sys.exit(1)
                    else:
                        umention_l = men_c
                        u_nmentions +=1
        counterl += 1
        if counterl % 1000000 == 0:
            print(counterl,'lines treated')
    #Print last line
    if ((u_nmentions * m_nmentions) > 0) or (full_mention > 0):
        if curdir == 0:
            fileout.write(str(uid)+','+str(mid)+','+str(umention_f)+','+str(umention_l)+','+str(mmention_f)+','+str(mmention_l)+','+str(u_nmentions)+','+str(m_nmentions))
            fileout.write('\n')
        else:
            fileout.write(str(mid)+','+str(uid)+','+str(umention_f)+','+str(umention_l)+','+str(mmention_f)+','+str(mmention_l)+','+str(u_nmentions)+','+str(m_nmentions))
            fileout.write('\n')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="Input file")
    parser.add_argument("-o","--output",
            type=argparse.FileType("w"),
            default=sys.stdout,
            help="Output file")
    parser.add_argument('--fullMentions',dest='full_mentions',action='store_true')
    parser.add_argument('--reciprocalMentions',dest='full_mentions',action='store_false')
    parser.set_defaults(full_mentions=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    getMentionList(args.input,args.output,args.full_mentions)
    args.input.close()
    args.output.close()

if __name__ == "__main__":
    main()

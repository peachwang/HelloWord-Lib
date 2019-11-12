# -*- coding: utf-8 -*-  
from File import File
from pydub import AudioSegment

class Audio(File) :

    def jsonSerialize(self) :
        return '{}'.format(self)

    # 可读化
    def j(self) :
        from util import j
        return j(self.jsonSerialize())

    def print(self, color = '') :
        from util import E
        print(color, self.j(), E if color != '' else '')
        return self

    def len(self) :
        pass

def wav2mp3(import_file_path, export_path = None, flog = None) :
    if flog is None : flog = sys.stdout
    time_format = '%Y-%m-%d %H:%M:%S'
    audio_path = import_file_path
    if audio_path[-4:] != '.wav' :
        flog.write('%s %s\n' % (strftime(time_format), 'ERROR: import file is not wav file.'))
        return 1
    elif not exists(audio_path) :
        flog.write('%s %s\n' % (strftime(time_format), 'ERROR: import file does not exist.'))
        return 2
    audio_path_wav = audio_path
    try :
        audio_wav = AudioSegment.from_file(audio_path_wav, format = 'wav')
    except Exception :
        flog.write('%s %s\n' % (strftime(time_format), 'ERROR: can not open import file.'))
        return 3

    audio_path = audio_path[:-4]
    file_name = audio_path.split('/')[-1]
    if export_path is None :
        path_name = audio_path[:len(audio_path) - len(file_name)]
    else :
        if not exists(export_path) :
            flog.write('%s %s\n' % (strftime(time_format), 'ERROR: export path does not exist.'))
            return 4
        path_name = export_path + '/'
    field_list = file_name.split('_')
    timestamp = field_list[-1]
    timestamp = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%m%d-%H%M%S')
    sentence_index = '第%02d句' % int(field_list[-2])
    length = '%02d秒' % (len(audio_wav) / 1000)
    field_list = [field_list[0]] + [field_list[1] + sentence_index, timestamp, length] + field_list[2:-2]
    audio_path_mp3 = (path_name + '_'.join(field_list) + '.mp3').encode('utf-8')

    # mp3_audio = mp3_audio[ start * 1000 : end * 1000 ]
    audio_wav.export(open(audio_path_mp3, 'wb'), format = 'mp3', bitrate = '32k', parameters = ['-ar', '44100', '-ac', '1'])
    # format = 'mp3', bitrate = '32k', parameters = ['-f', 'mp3', '-b', '32' , '-ar', '44100', '-ab', '16', '-ac', '1']
    flog.write('%s OK : %4dK %s exported from %s\n' % (strftime(time_format), getsize(audio_path_mp3) / 1024, audio_path_mp3, import_file_path))
    return 0

if __name__ == '__main__':
    print('hello')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
    import_file_path, export_path = sys.argv[1], sys.argv[2]
    print(import_file_path, export_path)
    print(u'\udce7')
    # exit(wav2mp3(import_file_path, export_path))
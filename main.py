# imports / packages
import os
import filetype
import videoprops
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener


# funcao que cria nomes padronizados para arquivos png ou jpg
def get_new_img_name(image):
    extension = filetype.guess_extension(image)
    image_file = Image.open(image)
    new_name = "-1"
    exif = {}
    try:
        if image_file.getexif() == None:
            new_name = "-1"
        else:
            for tag, value in image_file.getexif().items():
                # print(f"Log: {tag}: {value}")
                if tag == 306:
                    pic_date = value
                    formatted_pic_date = pic_date.replace(":", "").replace(" ", "")
                    new_name = f"img_{formatted_pic_date[:8]}_{formatted_pic_date[8:]}.{extension}"
    except KeyError:
        print(f"Log: Erro ao tentar acessar propriedades do arquivo {image}")
        new_name = "-1"
    return new_name


# funcao que cria nomes padronizados para arquivos heic
def get_new_heic_img_name(image):
    register_heif_opener()
    image_file = Image.open(image)
    new_name = "-1"
    exif = {}
    try:
        if image_file.getexif() == None:
            new_name = "-1"
        else:
            for tag, value in image_file.getexif().items():
                if tag == 306:
                    pic_date = value
                    formatted_pic_date = pic_date.replace(":", "").replace(" ", "")
                    new_name = f"img_{formatted_pic_date[:8]}_{formatted_pic_date[8:]}.{extension}"
    except KeyError:
        print(f"Log: Erro ao tentar acessar propriedades do arquivo {image}")
        new_name = "-1"
    return new_name


# funcao que cria nomes padronizados para arquivos mp4 ou mov
def get_new_vid_name(video):
    extension = filetype.guess_extension(video)
    properties = videoprops.get_video_properties(video)
    vid_date = properties['tags']['creation_time']
    formated_vid_date = vid_date.replace("-", "").replace("T", "").replace(":", "")
    new_name = f"vid_{formated_vid_date[:8]}_{formated_vid_date[8:14]}.{extension}"
    return new_name


# verifica se o arquivo destino ja existe no diretorio destino. Se existir, o arquivo deve ser renomeado. Caso
# contrário, o arquivo permanece com o nome anteriormente criado.
def generate_new_destination_pic(path, path2, file_name, old_file_name):
    number = 2
    name = file_name.split('.')[0]
    final_file = path + "\\" + file_name
    extension = filetype.guess_extension(path2 + "\\" + old_file_name)

    while 1 == 1:
        if os.path.exists(final_file):
            array_file_name = name.split('_')
            if len(array_file_name) == 3:
                new_name = f"{array_file_name[0]}_{array_file_name[1]}_{array_file_name[2]}_{number}.{extension}"
                name = new_name
            else:
                number = number + 1
                new_name = f"{array_file_name[0]}_{array_file_name[1]}_{array_file_name[2]}_{number}.{extension}"
                name = new_name
            final_file = path + "\\" + new_name
        else:
            break

    return final_file


# cria o diretório padronizado, baseado na data e horario em que a imagem foi capturada
def create_new_path(year, month, path):
    new_dir = path + "\\" + year + "\\" + month
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    return new_dir


# retorna a data e o horario em que a imagem foi capturada
def get_year_month(image):
    date = image[4:8]
    time = image[8:10]
    date_time = (date, time)
    return date_time


# main
source_path = "D:\\vitormontich\\imagens\\phone_media_organizer\\source"
destination_path = "D:\\vitormontich\\imagens\\phone_media_organizer\\destination"
problem_path = "D:\\vitormontich\\imagens\\phone_media_organizer\\destination\\problem"
enable_detailed_log = 0;

# loop em todos os arquivos do diretorio origem
for file in os.listdir(source_path):
    print(f"Log: Processando arquivo {file}")
    new_file_name = ""
    source_file = source_path + "\\" + file
    extension = filetype.guess_extension(source_file)
    # para cada tipo de arquivo / extensao, uma acao sera tomada
    if extension == "jpg" or extension == "png":
        # gera nome padronizado para imagem do tipo png ou jpg
        new_file_name = get_new_img_name(source_file)
    elif extension == "heic":
        # gera nome padronizado para imagem do heic
        new_file_name = get_new_heic_img_name(source_file)
    elif extension == "mov" or extension == "mp4":
        # gera nome padronizado para video do tipo mp4 ou mov
        new_file_name = get_new_vid_name(source_file)
    else:
        new_file_name = "-1"
        print("Log: Extensão não suportada")
    # se o nome gerado for '-1', o sistema ainda não processa arquivos da extensao em questao
    if new_file_name == "-1":
        destination_pic = problem_path + "\\" + file
        os.rename(source_file, destination_pic)
        print(f"Arquivo {file} nao foi movido corretamente. Verifique a pasta destination/problem")
    # se o nome gerado nao for '-1', o sistema conseguira processar o arquivo, alterar seu nome e enviar para o destino correto
    else:
        year_month = get_year_month(new_file_name)
        new_destination_path = create_new_path(year_month[0], year_month[1], destination_path)
        destination_pic = generate_new_destination_pic(new_destination_path, source_path, new_file_name, file)
        try:
            os.rename(source_file, destination_pic)
        except FileExistsError:
            print("Nao foi possivel mover o arquivo pois ele ja existe na pasta destino.")

import boto3
#from kubernetes import k8s_client, k8s_config
from functions import *

client = boto3.client('eks')

def select_cluster():
    clusters = client.list_clusters()
    listed_clusters = ''
    for i in range(len(clusters['clusters'])):
        listed_clusters = listed_clusters + f'{i} - {clusters["clusters"][i]}\n'
    try:
        print(listed_clusters)
        selected_cluster = int(input('Selecione o seu cluster (apenas números): ').strip())
    except:
        print('Algo deu errado!')
    return clusters['clusters'][selected_cluster]

if __name__ == '__main__':
    print('\n---> EKS Assessment tool <---\n')
    selected_cluster = select_cluster()
    directory_path = f'{os.getcwd()}/markdown'
    file_path=f'{directory_path}/{selected_cluster}.md'

    if check_if_exists(directory_path, file_path):
        while True:
            answer = input(f'O arquivo ./markdown/{selected_cluster}.md já existe. Deseja excluí-lo e realizar o assessment do zero? (s/n): ')
            if answer.lower() == 's':
                os.remove(file_path)
                break
            elif answer.lower() == 'n':
                break
            else:
                print("Não entendi. Insira 's' ou 'n'.")

    describe_cluster(selected_cluster)
    get_nodes(selected_cluster)

    print('Assessment realizado com sucesso!')
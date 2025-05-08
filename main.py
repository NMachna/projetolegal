import empresas
import licencas
import tags


def menu_empresas():
    while True:
        print("\nMENU - Empresas")
        print("1 - Cadastrar Empresa")
        print("2 - Consultar Empresa")
        print("3 - Editar Empresa")
        print("4 - Editar Datas de Licenças")
        print("5 - Atribuir Tag ou Licença")
        print("6 - Excluir Empresa")
        print("7 - Desassociar Licença de Empresa")
        print("8 - Voltar para o Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            empresas.cadastrar_empresa()
        elif opcao == "2":
            empresas.consultar_empresa()
        elif opcao == "3":
            empresas.editar_empresa()
        elif opcao == "4":
            empresas.editar_datas_licencas_empresa()
        elif opcao == "5":
            empresas.associar_empresa_a_tag_ou_licenca()
        elif opcao == "6":
            empresas.excluir_empresa()
        elif opcao == "7":
            empresas.desassociar_licenca_empresa()
        elif opcao == "8":
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_licencas():
    while True:
        print("\nMENU - Licenças")
        print("1 - Cadastrar Licença")
        print("2 - Excluir Licença")
        print("3 - Voltar para o Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            licencas.adicionar_licenca()
        elif opcao == "2":
            licencas.excluir_licenca()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_tags():
    while True:
        print("\nMENU - TAGs")
        print("1 - Adicionar TAG")
        print("2 - Excluir TAG")
        print("3 - Remover TAG de Empresa")
        print("4 - Voltar para o Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome_tag = input("Digite o nome da nova TAG: ")
            tags.cadastrar_tag(nome_tag)
        elif opcao == "2":
            nome_tag = input("Digite o nome da TAG a ser excluída: ")
            tags.excluir_tag(nome_tag)
        elif opcao == "3":
            tags.remover_tag_de_empresa()
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

#====================================================================================================================================================================================

def main():
    while True:
        print("\nMENU PRINCIPAL")
        print("1 - Empresas")
        print("2 - Licenças")
        print("3 - TAGs")
        print("4 - Sair do Sistema")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            menu_empresas()
        elif escolha == "2":
            menu_licencas()
        elif escolha == "3":
            menu_tags()
        elif escolha.lower() == "4" or escolha.lower() == "parar":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
import json
import sys
from pathlib import Path

# ============================================================
# IMPORTS DOS MÉTODOS DO BOT
# ============================================================
# Aqui você importa a função principal do seu bot.
# Exemplo:
# from aviso_notas_ppi_metodo import executar_envio
# from meu_bot import executar_bot


def ler_payload_task():
    """
    Lê o arquivo JSON temporário enviado pelo orquestrador.

    O orquestrador executa o bot passando o caminho do arquivo como argumento:
    python main.py C:\caminho\temporario\payload.json
    """
    try:
        task_file = None

        if len(sys.argv) > 1:
            task_file = sys.argv[1]

        if not task_file:
            raise ValueError("Nenhum arquivo de payload foi informado pelo orquestrador.")

        path = Path(task_file)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo de payload não encontrado: {task_file}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        raise RuntimeError(f"Erro ao ler payload da task: {e}")


def extrair_parametros(payload):
    """
    Extrai os parâmetros enviados pelo orquestrador.

    Padrão esperado:
    payload["parameters"][0]["parameter_value"]

    O campo parameter_value normalmente vem como string JSON.
    """
    try:
        if "parameters" not in payload or not payload["parameters"]:
            raise ValueError("Payload não possui parâmetros.")

        param = payload["parameters"][0]
        params_json = json.loads(param["parameter_value"])

        return params_json

    except Exception as e:
        raise RuntimeError(f"Erro ao extrair parâmetros do payload: {e}")


def executar_processo(params_json):
    """
    Função que chama a regra principal do bot.

    Coloque aqui a chamada para o método real do seu bot.
    """
    try:
        print("Iniciando processamento principal do bot...")
        print("BOT Teste Version: 1.0.0")

        email = params_json["dados_acesso"]["email"]
        senha = params_json["dados_acesso"]["senha"]

        print(f"E-mail recebido para execução: {email}")
        print(f"Senha recebido para execução: {senha}")

        # Exemplo de chamada real:
        # resultado = executar_envio(
        #     remetente_email=email,
        #     senha_email=senha,
        #     excel_path="Lista de email_2.xlsx",
        # )

        resultado = {
            "status": "success",
            "mensagem": "Bot executado com sucesso.",
        }

        return resultado

    except Exception as e:
        raise RuntimeError(f"Erro durante execução principal do bot: {e}")


def main():
    """
    Função principal chamada pelo orquestrador.
    """
    print("INICIANDO BOT PELO ORQUESTRADOR")

    payload = ler_payload_task()
    params_json = extrair_parametros(payload)
    resultado = executar_processo(params_json)

    print("RESULTADO DA EXECUÇÃO")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        erro = {
            "status": "error",
            "mensagem": str(e),
        }

        print("\n[ERRO]")
        print(json.dumps(erro, indent=4, ensure_ascii=False))

        # Obrigatório: retorna erro para o orquestrador.
        sys.exit(1)

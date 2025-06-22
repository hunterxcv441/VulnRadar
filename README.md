# VulnRadar

<img width="680" alt="image" src="https://github.com/user-attachments/assets/20753632-d37f-4ddc-9168-fb055a2c7b5a" />

📋 **Sobre**  
O VulnRadar é uma ferramenta de análise de segurança projetada para:  
- Baixar arquivos JavaScript de um site.  
- Identificar possíveis vulnerabilidades em arquivos JS.  
- Encontrar e verificar endpoints dentro do código.  
- Gerar relatórios detalhados em formatos TXT e JSON.  

---

## 🚀 **Funcionalidades**  
- **Download de Arquivos JS**: Realiza o download de todos os arquivos JavaScript de uma URL especificada.
- **Análise de Vulnerabilidades**: Verifica os arquivos JS em busca de padrões de vulnerabilidades conhecidos.
- **Identificação de Endpoints**: Detecta possíveis endpoints presentes no código JavaScript.
- **Geração de Relatórios**: Produz relatórios detalhados em formatos TXT e JSON para fácil interpretação.
- **Scripts Inline**: Extrai e salva também os blocos de JavaScript inline das páginas visitadas.
- **Filtro de Severidade**: Permite definir o nível mínimo de severidade a ser exibido nos relatórios.

---

## 🛠️ **Tecnologias Utilizadas**  
- Python 3  
- Requests  
- BeautifulSoup  
- TQDM  

---

## 📦 **Instalação**  
1. Clone o repositório:  
   ```bash
   git clone https://github.com/hunterxcv441/vulnradar.git
   cd vulnradar
Instale as dependências:

```bash
pip install -r requirements.txt
```
🖥️ Uso
help
   ```bash
WebScanner - JavaScript Vulnerability and Endpoint Analyzer

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL to scan for JavaScript files (default: None)
  -d DIRECTORY, --directory DIRECTORY
                        Directory to scan for JavaScript files (default: None)
  -p PATTERNS, --patterns PATTERNS
                        JSON file containing vulnerability patterns (default: /mnt/c/Users/RighiBuch/PycharmProjects/VulnRadar/webscanner/patterns.json) (default:
                        /mnt/c/Users/RighiBuch/PycharmProjects/VulnRadar/webscanner/patterns.json)
  -o OUTPUT, --output OUTPUT
                        Directory to save reports (default: ./results)
  -v, --verify-endpoints
                        Verify HTTP status codes for found endpoints (default: False)
  --min-severity {LOW,MEDIUM,HIGH}
                        Minimum severity level to include in reports (default: LOW)

```

🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um PR ou Issue no repositório.

📜 Licença
Este projeto está licenciado sob a MIT License.

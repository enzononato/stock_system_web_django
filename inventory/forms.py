# inventory/forms.py

from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    """
    Este ModelForm cria um formulário web
    automaticamente a partir do nosso modelo 'Item'.
    """

    # 1. MÉTODO __init__ para campos comuns
    def __init__(self, *args, **kwargs):
        """
        Este método é chamado assim que o formulário é criado.
        Vamos usá-lo para tornar os campos comuns obrigatórios.
        """
        super().__init__(*args, **kwargs)
        
        # Lista de campos que são sempre obrigatórios
        common_required_fields = [
            'brand', 
            'model', 
            'revenda', 
            'nota_fiscal', 
            'fornecedor', 
            'date_registered'
        ]
        
        for field_name in common_required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

    # 2. MÉTODO clean para validação dinâmica
    def clean(self):
        """
        Este método é chamado durante a validação do formulário.
        Vamos usá-lo para tornar os campos específicos obrigatórios
        com base no 'tipo' selecionado.
        
        Esta lógica é a "tradução" da sua validação no cmd_add do gui.py
       
        """
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')

        if not tipo:
            # Se o tipo não foi selecionado, não podemos validar
            # (o campo 'tipo' já será marcado como obrigatório pelo __init__ ou Meta)
             self.add_error('tipo', 'Este campo é obrigatório.')
             return cleaned_data

        # --- Validação Dinâmica por Tipo ---

        if tipo == 'Celular':
            if not cleaned_data.get('identificador'):
                self.add_error('identificador', 'IMEI é obrigatório para Celular.')
        
        elif tipo == 'Notebook' or tipo == 'Desktop':
            fields_to_check = {
                'dominio': 'Domínio', 'host': 'Host', 'endereco_fisico': 'Endereço Físico',
                'storage': 'Armazenamento', 'sistema': 'Sistema Operacional', 'cpu': 'Processador',
                'ram': 'Memória RAM', 'licenca': 'Licença Windows', 'anydesk': 'AnyDesk'
            }
            for field_name, label in fields_to_check.items():
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, f'{label} é obrigatório para Notebook/Desktop.')

        elif tipo == 'Impressora':
            fields_to_check = {'setor': 'Setor', 'ip': 'IP', 'mac': 'MAC'}
            for field_name, label in fields_to_check.items():
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, f'{label} é obrigatório para Impressora.')

        elif tipo == 'Tablet':
            if not cleaned_data.get('identificador'):
                self.add_error('identificador', 'Nº de Série é obrigatório para Tablet.')
            if not cleaned_data.get('storage'):
                self.add_error('storage', 'Armazenamento é obrigatório para Tablet.')

        elif tipo == 'Switch':
            if not cleaned_data.get('poe'):
                self.add_error('poe', 'O campo POE é obrigatório para Switch.')
            if not cleaned_data.get('quantidade_portas'):
                self.add_error('quantidade_portas', 'Quantidade de Portas é obrigatório para Switch.')

        elif tipo == 'HD':
            if not cleaned_data.get('storage'):
                self.add_error('storage', 'Armazenamento é obrigatório para HD.')

        elif tipo == 'Nobreak':
            fields_to_check = {
                'identificador': 'Número de Série', 'codigo_patrimonial': 'Código Patrimonial',
                'responsavel': 'Responsável', 'potencia_nominal': 'Potência Nominal',
                'autonomia_estimada': 'Autonomia Estimada'
            }
            for field_name, label in fields_to_check.items():
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, f'{label} é obrigatório para Nobreak.')

        elif tipo == 'Access Point':
            fields_to_check = {
                'identificador': 'Número de Série', 'codigo_patrimonial': 'Código Patrimonial',
                'local_instalacao': 'Local da Instalação', 'setor': 'Setor',
                'ip': 'IP', 'mac': 'MAC'
            }
            for field_name, label in fields_to_check.items():
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, f'{label} é obrigatório para Access Point.')
        
        return cleaned_data


    # 3. CLASSE Meta (permanece a mesma)
    class Meta:
        model = Item
        
        # A lista de 'fields' continua a mesma
        fields = [
            'tipo', 
            'brand', 
            'model', 
            'identificador',
            'nota_fiscal',
            'revenda',
            'fornecedor',
            'date_registered',
            # Campos técnicos
            'dominio',
            'host',
            'endereco_fisico',
            'cpu',
            'ram',
            'storage',
            'sistema',
            'licenca',
            'anydesk',
            'setor',
            'ip',
            'mac',
            # Campos de Nobreak
            'potencia_nominal',
            'autonomia_estimada',
            'ip_snmp',
            'codigo_patrimonial',
            'responsavel',
            # Campos de Access Point
            'local_instalacao',
            # Campos de Switch
            'poe',
            'quantidade_portas',
        ]

        # Os 'widgets' continuam os mesmos
        widgets = {
            'date_registered': forms.DateInput(attrs={'type': 'date'}),
        }
import fitz
import pdfplumber
import re


class TBankPDFParser:
    def merge_amount_parts(self, parts):
        merged = []
        skip_next = False
        for i in range(len(parts)):
            if skip_next:
                skip_next = False
                continue
            if i + 1 < len(parts):
                # Проверяем, что текущий элемент начинается с + или - и следующий элемент - число с точкой
                if (parts[i].startswith(('+', '-')) and
                        re.match(r'^\d+(\.\d+)?$', parts[i + 1].replace(' ', ''))):
                    merged.append(parts[i] + parts[i + 1])
                    skip_next = True
                else:
                    merged.append(parts[i])
            else:
                merged.append(parts[i])
        return merged

    def parse_pdf(self, file_path):
        transactions = []
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        lines = text.split('\n')
        start_index = 0
        for i, line in enumerate(lines):
            if 'Дата и время операции' in line:
                start_index = i + 1
                break

        i = start_index
        while i < len(lines) - 1:
            line = lines[i]
            next_line = lines[i + 1]

            # Разбиваем строки на части и объединяем части суммы
            parts = self.merge_amount_parts(line.split())
            next_parts = self.merge_amount_parts(next_line.split())

            if re.match(r'^\d{2}\.\d{2}\.\d{4}', parts[0]):
                if len(parts) >= 2:
                    date_str = parts[0]
                    debit_date_str = parts[1]
                    # Берём описание с 6 по предпоследний элемент
                    description_str = ' '.join(parts[6:-1]) if len(parts) > 7 else ''
                    operation_time = next_parts[0] if len(next_parts) > 0 else ''
                    debit_time = next_parts[1] if len(next_parts) > 1 else ''
                    description_next = ' '.join(next_parts[2:]) if len(next_parts) > 2 else ''
                    number_card = parts[-1]
                    remaining_text = ' '.join(parts[2:])
                    # Ищем сумму с валютой дважды
                    amount_match = re.findall(r'([+-]?\d+(\.\d+)?\s*[₽$€])', remaining_text)
                    if len(amount_match) >= 2:
                        amount_operation = amount_match[0][0]
                        amount_card = amount_match[1][0]
                    else:
                        amount_operation = ' '.join(parts[2:4]) if len(parts) > 3 else ''
                        amount_card = ' '.join(parts[4:6]) if len(parts) > 5 else ''
                    transactions.append({
                        'date': f"{date_str}\n{operation_time}",
                        'time': f"{debit_date_str}\n{debit_time}",
                        'amount_operation_currency': amount_operation,
                        'amount_card_currency': amount_card,
                        'description': f"{description_str} {description_next}".strip(),
                        'number_card': number_card,
                    })
                    i += 2
                    continue
            i += 1

        return transactions


class AlfaBankPDFParser:
    """Парсер для Альфа банка с нужными колонками"""
    def parse_pdf(self, file_path):
        doc = fitz.open(file_path)
        transactions = []
        for page in doc:
            text = page.get_text()
            lines = text.split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) >= 4:
                    transactions.append({
                        'posting_date': parts[0],
                        'operation_code': parts[1],
                        'description': parts[2],
                        'amount': parts[3]
                    })
        return transactions
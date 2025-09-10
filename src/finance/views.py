import tempfile
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .pdf_parsers import TBankPDFParser, AlfaBankPDFParser


@login_required
def index(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'transactions': transactions})


def safe_decimal(value):
    try:
        return Decimal(str(value).replace(',', '.').strip())
    except (InvalidOperation, ValueError, AttributeError):
        return Decimal('0')  # или None, в зависимости от логики


def serialize_transaction_data(data):
    from datetime import date, datetime
    new_data = {}
    for key, value in data.items():
        if isinstance(value, (date, datetime)):
            new_data[key] = value.isoformat()
        else:
            new_data[key] = value
    return new_data


@login_required
def import_transactions(request):
    error = None
    transactions = []
    bank = ''
    if request.method == "POST":
        file = request.FILES.get('pdf_file')
        bank = request.POST.get('bank', '')
        if not file or bank not in ['tbank', 'alfabank']:
            error = "Выберите файл и банк"
        else:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                temp_path = tmp_file.name

            if bank == 'tbank':
                parser = TBankPDFParser()
                transactions = parser.parse_pdf(temp_path)
            elif bank == 'alfabank':
                parser = AlfaBankPDFParser()
                transactions = parser.parse_pdf(temp_path)

            account, _ = Account.objects.get_or_create(
                user=request.user,
                name=f"Импортированный счёт {bank}",
                defaults={'account_type': 'card'}
            )
            print(account)
            for tr in transactions:
                if bank == 'tbank':
                    try:
                        amount = tr.get('amount_card_currency', Decimal('0'))
                        date = tr.get('date')
                        time = tr.get('time')
                        description = tr.get('description', '')
                        serialized_data = serialize_transaction_data(tr)

                        Transaction.objects.create(
                            user=request.user,
                            account=account,
                            amount=amount,
                            description=description,
                            date=date,
                            time=time,
                            status='OK',
                            original_data=serialized_data
                        )
                    except Exception:
                        # Логировать ошибку при необходимости
                        continue
                else:
                    # Аналогично для alfbank, если нужно
                    amount = safe_decimal(tr.get('amount', 0))
                    Transaction.objects.create(
                        user=request.user,
                        account=account,
                        amount=amount,
                        description=tr.get('description', ''),
                        date=tr.get('posting_date'),
                        status='OK',
                        original_data=tr
                    )
            return render(request, 'transactions/import_result.html',
                          {'transactions': transactions, 'bank': bank})

    return render(request, 'transactions/import.html', {'error': error, 'bank': bank})


@login_required
@require_POST
def clear_transactions(request):
    count = Transaction.objects.filter(user=request.user).delete()[0]
    return redirect('dashboard')

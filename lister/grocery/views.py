from django.shortcuts import render
from django.http import HttpResponse
import csv
import weasyprint
from django.template.loader import render_to_string

def load_grocery_data():
    groceries = []
    with open('grocery/data/BigBasket.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            groceries.append({
                'index': row['index'],
                'product': row['product'],
                'category': row['category'],
                'sub_category': row['sub_category'],
            })
    return groceries

def generate_pdf(selected_items):
    # Render HTML template to string
    html_content = render_to_string('lister/pdf_template.html', {'items': selected_items})
    
    # Convert HTML to PDF using WeasyPrint
    pdf_file = weasyprint.HTML(string=html_content).write_pdf()

    # Create response to return the PDF as a download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="grocery_list.pdf"'
    return response

def home(request):
    groceries = load_grocery_data()

    # Get search and category filter values
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    sub_category_filter = request.GET.get('sub_category', '').strip()

    # Filter by search query if provided
    if search_query:
        groceries = [item for item in groceries if search_query.lower() in item['product'].lower()]

    # Filter by category if provided
    if category_filter:
        groceries = [item for item in groceries if category_filter.lower() in item['category'].lower()]

    # Filter by sub-category if provided
    if sub_category_filter:
        groceries = [item for item in groceries if sub_category_filter.lower() in item['sub_category'].lower()]

    # Handle form submission (quantity selection)
    if request.method == 'POST':
        selected_items = []
        for item in groceries:
            quantity = request.POST.get(f'quantity_{item["index"]}')
            if quantity and int(quantity) > 0:
                selected_items.append({
                    'product': item['product'],
                    'category': item['category'],
                    'sub_category': item['sub_category'],
                    'quantity': quantity,
                })

        # If there are selected items, generate a PDF file for download
        if selected_items:
            return generate_pdf(selected_items)

        # If no items were selected, return a message
        return render(request, 'home.html', {
            'groceries': groceries,
            'search_query': search_query,
            'category_filter': category_filter,
            'sub_category_filter': sub_category_filter,
            'message': 'No items selected or quantity is invalid.',
        })

    return render(request, 'home.html', {
        'groceries': groceries,
        'search_query': search_query,
        'category_filter': category_filter,
        'sub_category_filter': sub_category_filter,
        'message': '',
    })

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AsyncOpenAI
from sql_metadata import Parser
import csv
from .secret import get_secret

ai_client = AsyncOpenAI(api_key=get_secret("openaikey1"))

async def create_excel_file(request):
    try:
        data = json.loads(request.body)
        sql_query = data.get('sql_query', '')

        if not sql_query:
            response_data = {
                'success': False,
                'message': 'SQL query is required.'
            }
            return JsonResponse(response_data, status=400, safe=False)

        description, csv_content = await generate_description_and_csv(sql_query)

        response_data = {
            'success': True,
            'message': 'CSV content created successfully.',
            'description': description,
            'csv_content': csv_content
        }
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        error_message = str(e)
        response_data = {
            'success': False,
            'message': 'An error occurred: ' + error_message
        }
        return JsonResponse(response_data, status=500, safe=False)


async def generate_description_and_csv(sql_query):
    prompt = f"Generate a description for the CSV content created based on the SQL query: {sql_query}"
    response = await ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    description = response.choices[0].message.content.strip()

    table_columns = Parser(sql_query).columns
    rw_tables = Parser(sql_query).tables
    places = Parser(sql_query).columns_dict
    tables = [t for t in rw_tables if t.strip() is not None]
    columns_stack = Parser(sql_query).columns

    csv_content = []
    csv_content.append(['Table Name', 'Column Name'])

    inserts = 1

    if len(tables) == 1:
        for i in range(len(table_columns)):
            if table_columns[i] in columns_stack:
                columns_stack.remove(table_columns[i])
            csv_content.append([tables[0], table_columns[i].replace(tables[0] + '.', '').strip()])
            inserts += 1
    else:
        for x in range(len(table_columns)):
            curr_column = table_columns[x]
            if curr_column is not None:
                for t in tables:
                    if t in curr_column:
                        csv_content.append([t, curr_column.replace(t + '.', '').strip()])
                        inserts += 1

        if len(columns_stack) > 0:
            for column in columns_stack:
                csv_content.append(['Unknown', column.strip()])
                inserts += 1

    return description, csv_content


@csrf_exempt
def download_csv(request):
    try:
        data = json.loads(request.body)
        csv_content = data.get('csv_content', [])
        if not csv_content:
            response_data = {
                'success': False,
                'message': 'CSV content is required.'
            }
            return JsonResponse(response_data, status=400, safe=False)

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="output.csv"'

        # Create CSV writer and write content
        csv_writer = csv.writer(response)
        csv_writer.writerows(csv_content)

        return response

    except Exception as e:
        error_message = str(e)
        response_data = {
            'success': False,
            'message': 'An error occurred: ' + error_message
        }
        return JsonResponse(response_data, status=500, safe=False)

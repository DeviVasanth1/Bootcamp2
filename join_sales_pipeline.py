import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json

class ParseJson(beam.DoFn):
    def process(self, element):
        try:
            yield json.loads(element)
        except:
            pass

def run():
    options = PipelineOptions(
        runner='DataflowRunner',
        project='de-practices',
        region='us-central1',
        temp_location='gs://retail-bronze-layer/temp/',
        staging_location='gs://retail-bronze-layer/staging/',
        job_name='join-sales-customers-products'
    )

    with beam.Pipeline(options=options) as p:

        # Read all three datasets
        sales = (
            p
            | 'Read Sales' >> beam.io.ReadFromText('gs://retail-silver-layer/sales_cleaned*.json')
            | 'Parse Sales JSON' >> beam.ParDo(ParseJson())
            | 'Map Sales by CustomerID-ProductID' >> beam.Map(lambda record: ((record['CustomerID'], record['ProductID']), record))
        )

        customers = (
            p
            | 'Read Customers' >> beam.io.ReadFromText('gs://retail-silver-layer/customers_cleaned*.json')
            | 'Parse Customers JSON' >> beam.ParDo(ParseJson())
            | 'Map Customers by CustomerID' >> beam.Map(lambda record: (record['CustomerID'], record))
        )

        products = (
            p
            | 'Read Products' >> beam.io.ReadFromText('gs://retail-silver-layer/products_cleaned_from_pg*.json')
            | 'Parse Products JSON' >> beam.ParDo(ParseJson())
            | 'Map Products by ProductID' >> beam.Map(lambda record: (record['ProductID'], record))
        )

        # Join Customers with Sales on CustomerID
        joined_sales_customers = (
            {'sales': sales, 'customers': customers}
            | 'Group by CustomerID' >> beam.CoGroupByKey()
            | 'Flatten Sales + Customer Info' >> beam.FlatMap(
                lambda kv: [
                    {
                        **sale,
                        'CustomerName': kv[1]['customers'][0]['CustomerName'],
                        'Email': kv[1]['customers'][0]['Email'],
                        'Country': kv[1]['customers'][0]['Country']
                    }
                    for sale in kv[1]['sales']
                ]
            )
            | 'Map by ProductID for Product Join' >> beam.Map(lambda record: (record['ProductID'], record))
        )

        # Join with Products on ProductID
        final_joined = (
            {'sales_customers': joined_sales_customers, 'products': products}
            | 'Group by ProductID' >> beam.CoGroupByKey()
            | 'Flatten All Joined Data' >> beam.FlatMap(
                lambda kv: [
                    {
                        **sale,
                        'ProductName': kv[1]['products'][0]['ProductName'],
                        'Category': kv[1]['products'][0]['Category'],
                        'Price': kv[1]['products'][0]['Price']
                    }
                    for sale in kv[1]['sales_customers']
                    if kv[1]['products']
                ]
            )
        )

        # Write to Cloud Storage as JSON
        (
            final_joined
            | 'To JSON Strings' >> beam.Map(lambda record: json.dumps(record))
            | 'Write Final Output' >> beam.io.WriteToText('gs://retail-gold-layer/joined_data', file_name_suffix='.json')
        )

if __name__ == '__main__':
    run()

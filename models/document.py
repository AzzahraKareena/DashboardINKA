import csv
import pymysql
import mysql.connector

class DocumentModel:
    def __init__(self):
        self.connection = pymysql.connect(

            host="36.94.112.123",  # IP server database
            user="it",             # Username database
            password="ITIMS321",   # Password database
            database="dashboard",  # Nama database
            port=3306              # Port MySQL (default: 3306)
        )
        
    def save_to_database(self, csv_file, selected_columns, table_name):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Read the header row

                # Prepare SQL insert statement
                sql_header = ', '.join([f"`{col}`" for col in selected_columns])
                insert_query = f"INSERT INTO {table_name} ({sql_header}) VALUES ({', '.join(['%s'] * len(selected_columns))})"

                for row in reader:
                    filtered_row = [row[header.index(col)] for col in selected_columns]
                    cursor.execute(insert_query, filtered_row)

            conn.commit()
            print("Data successfully inserted into the database.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    def insert_document(self, filename, file_type):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO Document (filename, file_type)
        VALUES (%s, %s)
        """
        cursor.execute(query, (filename, file_type))
        self.connection.commit()
        document_id = cursor.lastrowid
        cursor.close()
        return document_id

    def insert_cn42n_data(self, project_definition, name):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO cn42n (`Project definition`, `Name`)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            `Project definition` = VALUES(`Project definition`),
            `Name` = VALUES(`Name`)
        """  
        try:
            cursor.execute(query, (project_definition, name))
            self.connection.commit()
            print("Data successfully inserted into the database.")  # Debugging line
        except Exception as e:
            print(f"Error inserting data into database: {str(e)}")  # Print any database errors
        finally:
            cursor.close()


    def insert_cn43n_data(self, project_definition, wbs_element, name, level, status):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO cn43n (`Project definition`, `WBS element`, `Name`, `Level`, `Status`)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `Project definition` = VALUES(`Project definition`),
            `WBS element` = VALUES(`WBS element`),
            `Name` = VALUES(`Name`),
            `Level` = VALUES(`Level`),
            `Status` = VALUES(`Status`);
        """
        cursor.execute(query, (project_definition, wbs_element, name, level, status))
        self.connection.commit()
        cursor.close()

    def insert_cn55n_data(self, project_definition, wbs_element, sales_document, sales_document_item):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO cn55n (`Project Definition`, `WBS Element`, `Sales Document`, `Sales Document Item`)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `Project Definition` = VALUES(`Project Definition`),
            `WBS Element` = VALUES(`WBS Element`),
            `Sales Document` = VALUES(`Sales Document`),
            `Sales Document Item` = VALUES(`Sales Document Item`);
        """
        cursor.execute(query, (project_definition, wbs_element, sales_document, sales_document_item))
        self.connection.commit()
        cursor.close()

    def insert_va05_data(self, sales_document, sales_document_type, document_date, purchase_order_number,
                          status, item_sd, description, material, confirmed_quantity, delivery_date,
                          created_by, sold_to_party, name_1, exchange_rate, order_quantity,
                          base_unit_of_measure, net_price, pricing_unit, unit_of_measure,
                          pricing_date, net_value, document_currency, goods_issue_date, created_on):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO VA05Data (`Sales Document`, `Sales Document Type`, `Document Date`, `Purchase order number`, 
                               `Status`, `Item (SD)`, `Description`, `Material`, `Confirmed Quantity`, 
                               `Delivery Date`, `Created by`, `Sold-to party`, `Name 1`, `Exchange Rate`, 
                               `Order Quantity`, `Base Unit of Measure`, `Net price`, `Pricing unit`, 
                               `Unit of measure`, `Pricing date`, `Net Value`, `Document Currency`, 
                               `Goods Issue Date`, `Created on`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `Sales Document` = VALUES(`Sales Document`),
            `Sales Document Type` = VALUES(`Sales Document Type`),
            `Document Date` = VALUES(`Document Date`),
            `Purchase order number` = VALUES(`Purchase order number`),
            `Status` = VALUES(`Status`),
            `Item (SD)` = VALUES(`Item (SD)`),
            `Description` = VALUES(`Description`),
            `Material` = VALUES(`Material`),
            `Confirmed Quantity` = VALUES(`Confirmed Quantity`),
            `Delivery Date` = VALUES(`Delivery Date`),
            `Created by` = VALUES(`Created by`),
            `Sold-to party` = VALUES(`Sold-to party`),
            `Name 1` = VALUES(`Name 1`),
            `Exchange Rate` = VALUES(`Exchange Rate`),
            `Order Quantity` = VALUES(`Order Quantity`),
            `Base Unit of Measure` = VALUES(`Base Unit of Measure`),
            `Net price` = VALUES(`Net price`),
            `Pricing unit` = VALUES(`Pricing unit`),
            `Unit of measure` = VALUES(`Unit of measure`),
            `Pricing date` = VALUES(`Pricing date`),
            `Net Value` = VALUES(`Net Value`),
            `Document Currency` = VALUES(`Document Currency`),
            `Goods Issue Date` = VALUES(`Goods Issue Date`),
            `Created on` = VALUES(`Created on`);
        """
        cursor.execute(query, (sales_document, sales_document_type, document_date, purchase_order_number,
                               status, item_sd, description, material, confirmed_quantity, delivery_date,
                               created_by, sold_to_party, name_1, exchange_rate, order_quantity,
                               base_unit_of_measure, net_price, pricing_unit, unit_of_measure,
                               pricing_date, net_value, document_currency, goods_issue_date, created_on))
        self.connection.commit()
        cursor.close()
    
    def insert_me5j_data(self, wbs_element, purchase_requisition, item_of_requisition, requisition_date,
                          deliv_date, deletion_indicator, processing_status, material, short_text,
                          material_group, requisitioner, purchasing_group, quantity_requested,
                          unit_of_measure, purchase_order, purchase_order_date, purchase_order_item,
                          quantity_ordered, document_type, storage_location):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO me5j (`WBS Element`, `Purchase Requisition`, `Item of Requisition`, `Requisition Date`,
                               `Deliv. date(From/to)`, `Deletion Indicator`, `Processing status`, `Material`,
                               `Short Text`, `Material Group`, `Requisitioner`, `Purchasing Group`,
                               `Quantity Requested`, `Unit of Measure`, `Purchase Order`, `Purchase Order Date`,
                               `Purchase Order Item`, `Quantity Ordered`, `Document Type`, `Storage Location`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `WBS Element` = VALUES(`WBS Element`),
            `Purchase Requisition` = VALUES(`Purchase Requisition`),
            `Item of Requisition` = VALUES(`Item of Requisition`),
            `Requisition Date` = VALUES(`Requisition Date`),
            `Deliv. date(From/to)` = VALUES(`Deliv. date(From/to)`),
            `Deletion Indicator` = VALUES(`Deletion Indicator`),
            `Processing status` = VALUES(`Processing status`),
            `Material` = VALUES(`Material`),
            `Short Text` = VALUES(`Short Text`),
            `Material Group` = VALUES(`Material Group`),
            `Requisitioner` = VALUES(`Requisitioner`),
            `Purchasing Group` = VALUES(`Purchasing Group`),
            `Quantity Requested` = VALUES(`Quantity Requested`),
            `Unit of Measure` = VALUES(`Unit of Measure`),
            `Purchase Order` = VALUES(`Purchase Order`),
            `Purchase Order Date` = VALUES(`Purchase Order Date`),
            `Purchase Order Item` = VALUES(`Purchase Order Item`),
            `Quantity Ordered` = VALUES(`Quantity Ordered`),
            `Document Type` = VALUES(`Document Type`),
            `Storage Location` = VALUES(`Storage Location`);
        """
        cursor.execute(query, (wbs_element, purchase_requisition, item_of_requisition, requisition_date,
                               deliv_date, deletion_indicator, processing_status, material, short_text,
                               material_group, requisitioner, purchasing_group, quantity_requested,
                               unit_of_measure, purchase_order, purchase_order_date, purchase_order_item,
                               quantity_ordered, document_type, storage_location))
        self.connection.commit()
        cursor.close()
    
    def insert_me2j_data(self, wbs_element, purchasing_document, item, material, deletion_indicator,
                          short_text, order_quantity, order_unit, document_date,
                          vendor_supplying_plant, still_to_be_delivered_value,
                          still_to_be_invoiced_qty, still_to_be_invoiced_val, net_price,
                          still_to_be_delivered_qty, currency, acct_assignment_cat,
                          po_history_release_documentation):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO me2j (`WBS Element`, `Purchasing Document`, `Item`, `Material`,
                               `Deletion Indicator`, `Short Text`, `Order Quantity`, `Order Unit`,
                               `Document Date`, `Vendor/supplying plant`, `Still to be delivered (value)`,
                               `Still to be invoiced (qty)`, `Still to be invoiced (val.)`, `Net price`,
                               `Still to be delivered (qty)`, `Currency`, `Acct Assignment Cat.`,
                               `PO history/release documentation`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `WBS Element` = VALUES(`WBS Element`),
            `Purchasing Document` = VALUES(`Purchasing Document`),
            `Item` = VALUES(`Item`),
            `Material` = VALUES(`Material`),
            `Deletion Indicator` = VALUES(`Deletion Indicator`),
            `Short Text` = VALUES(`Short Text`),
            `Order Quantity` = VALUES(`Order Quantity`),
            `Order Unit` = VALUES(`Order Unit`),
            `Document Date` = VALUES(`Document Date`),
            `Vendor/supplying plant` = VALUES(`Vendor/supplying plant`),
            `Still to be delivered (value)` = VALUES(`Still to be delivered (value)`),
            `Still to be invoiced (qty)` = VALUES(`Still to be invoiced (qty)`),
            `Still to be invoiced (val.)` = VALUES(`Still to be invoiced (val.)`),
            `Net price` = VALUES(`Net price`),
            `Still to be delivered (qty)` = VALUES(`Still to be delivered (qty)`),
            `Currency` = VALUES(`Currency`),
            `Acct Assignment Cat.` = VALUES(`Acct Assignment Cat.`),
            `PO history/release documentation` = VALUES(`PO history/release documentation`);
        """
        cursor.execute(query, (wbs_element, purchasing_document, item, material, deletion_indicator,
                               short_text, order_quantity, order_unit, document_date,
                               vendor_supplying_plant, still_to_be_delivered_value,
                               still_to_be_invoiced_qty, still_to_be_invoiced_val, net_price,
                               still_to_be_delivered_qty, currency, acct_assignment_cat,
                               po_history_release_documentation))
        self.connection.commit()
        cursor.close()


    def insert_mb51_gr_data(self, data):
        query = """
        INSERT INTO mb51_gr (
            `Posting Date`, `Material`, `Material Description`, `Purchase Order`, 
            `Document Date`, `Qty in Un. of Entry`, `Item GR`, `Movement Type`, 
            `WBS Element`, `Unit of Entry`, `Item PO`, `Amount in LC`, 
            `Material Document`, `User Name`, `Document Header Text`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('Posting Date', None), data.get('Material', None), data.get('Material Description', None), 
            data.get('Purchase Order', None), data.get('Document Date', None), 
            data.get('Qty in Un. of Entry', None), data.get('Item GR', None), 
            data.get('Movement Type', None), data.get('WBS Element', None), 
            data.get('Unit of Entry', None), data.get('Item PO', None), 
            data.get('Amount in LC', None), data.get('Material Document', None), 
            data.get('User Name', None), data.get('Document Header Text', None)
        )

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()  # Rollback jika terjadi kesalahan
            print(f"Error saat memasukkan data ke mb51_gr: {e}")
            raise  # Optional: kembali mengirimkan error untuk ditangani di tempat lain
        finally:
            if cursor:
                cursor.close()



    def insert_mb51_gi_data(self, posting_date, material, material_description, purchase_order,
                                    document_date, qty_in_unit_of_entry, item, movement_type,
                                    wbs_element, unit_of_entry, amount_in_lc, material_document,
                                    user_name, document_header_text, reference, order,
                                    vendor, reservation, batch):
                cursor = self.connection.cursor()
                query = """
                INSERT INTO mb51_gi (`Posting Date`, `Material`, `Material Description`, `Purchase Order`,
                                        `Document Date`, `Qty in Un. of Entry`, `Item`, `Movement Type`,
                                        `WBS Element`, `Unit of Entry`, `Amount in LC`, `Material Document`,
                                        `User Name`, `Document Header Text`, `Reference`, `Order`,
                                        `Vendor`, `Reservation`, `Batch`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    `Posting Date` = VALUES(`Posting Date`),
                    `Material` = VALUES(`Material`),
                    `Material Description` = VALUES(`Material Description`),
                    `Purchase Order` = VALUES(`Purchase Order`),
                    `Document Date` = VALUES(`Document Date`),
                    `Qty in Un. of Entry` = VALUES(`Qty in Un. of Entry`),
                    `Item` = VALUES(`Item`),
                    `Movement Type` = VALUES(`Movement Type`),
                    `WBS Element` = VALUES(`WBS Element`),
                    `Unit of Entry` = VALUES(`Unit of Entry`),
                    `Amount in LC` = VALUES(`Amount in LC`),
                    `Material Document` = VALUES(`Material Document`),
                    `User Name` = VALUES(`User Name`),
                    `Document Header Text` = VALUES(`Document Header Text`),
                    `Reference` = VALUES(`Reference`),
                    `Order` = VALUES(`Order`),
                    `Vendor` = VALUES(`Vendor`),
                    `Reservation` = VALUES(`Reservation`),
                    `Batch` = VALUES(`Batch`);
                """
                cursor.execute(query, (posting_date, material, material_description, purchase_order,
                                    document_date, qty_in_unit_of_entry, item, movement_type,
                                    wbs_element, unit_of_entry, amount_in_lc, material_document,
                                    user_name, document_header_text, reference, order,
                                    vendor, reservation, batch))
                self.connection.commit()
                cursor.close()     

    def insert_mb52_data(self, posting_date, material, material_description, purchase_order,
                            document_date, qty_in_unit_of_entry, item, movement_type,
                            wbs_element, unit_of_entry, amount_in_lc, material_document,
                            user_name, document_header_text):
            cursor = self.connection.cursor()
            query = """
            INSERT INTO mb52 (`Posting Date`, `Material`, `Material Description`, `Purchase Order`,
                            `Document Date`, `Qty in Un. of Entry`, `Item`, `Movement Type`,
                            `WBS Element`, `Unit of Entry`, `Amount in LC`, `Material Document`,
                            `User Name`, `Document Header Text`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                `Posting Date` = VALUES(`Posting Date`),
                `Material` = VALUES(`Material`),
                `Material Description` = VALUES(`Material Description`),
                `Purchase Order` = VALUES(`Purchase Order`),
                `Document Date` = VALUES(`Document Date`),
                `Qty in Un. of Entry` = VALUES(`Qty in Un. of Entry`),
                `Item` = VALUES(`Item`),
                `Movement Type` = VALUES(`Movement Type`),
                `WBS Element` = VALUES(`WBS Element`),
                `Unit of Entry` = VALUES(`Unit of Entry`),
                `Amount in LC` = VALUES(`Amount in LC`),
                `Material Document` = VALUES(`Material Document`),
                `User Name` = VALUES(`User Name`),
                `Document Header Text` = VALUES(`Document Header Text`);
            """
            try:
                cursor.execute(query, (posting_date, material, material_description, purchase_order,
                                    document_date, qty_in_unit_of_entry, item, movement_type,
                                    wbs_element, unit_of_entry, amount_in_lc, material_document,
                                    user_name, document_header_text))
                self.connection.commit()
            except Exception as e:
                self.connection.rollback()  # Rollback if there is an error
                print(f"Error inserting data into mb52: {e}")
                raise  # Optional: raise the exception to handle it elsewhere
            finally:
                cursor.close()
        
    def insert_mb52_data(self, csv_file):
            cursor = self.connection.cursor()
            
            # Delete existing data in MB52 table
            cursor.execute("DELETE FROM MB52")
            self.connection.commit()

            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sql = """
                    INSERT INTO MB52 (Material, Plnt, SLoc, S, `Special stock number`, BUn, Unrestricted, Crcy, `Value Unrestricted`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        Plnt = VALUES(Plnt),
                        SLoc = VALUES(SLoc),
                        S = VALUES(S),
                        `Special stock number` = VALUES(`Special stock number`),
                        BUn = VALUES(BUn),
                        Unrestricted = VALUES(Unrestricted),
                        Crcy = VALUES(Crcy),
                        `Value Unrestricted` = VALUES(`Value Unrestricted`);
                    """
                    cursor.execute(sql, (
                        row['Material'], row['Plnt'], row['SLoc'], row['S'],
                        row['Special stock number'], row['BUn'], row['Unrestricted'], row['Crcy'], row['Value Unrestricted']
                    ))

            self.connection.commit()
            cursor.close()

    def insert_matspec_data(self, material, material_description, text_chars, base_unit_of_measure, 
                            material_group, material_type, plant, df_at_client_level, 
                            valuation_class, created_by, last_change, price):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO matspec (`Material`, `Material Description`, `Text (Chars 200.)`, 
                            `Base Unit of Measure`, `Material Group`, `Material Type`, 
                            `Plant`, `DF at client level`, `Valuation Class`, 
                            `Created by`, `Last change`, `Price`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            `Material Description` = VALUES(`Material Description`),
            `Text (Chars 200.)` = VALUES(`Text (Chars 200.)`),
            `Base Unit of Measure` = VALUES(`Base Unit of Measure`),
            `Material Group` = VALUES(`Material Group`),
            `Material Type` = VALUES(`Material Type`),
            `Plant` = VALUES(`Plant`),
            `DF at client level` = VALUES(`DF at client level`),
            `Valuation Class` = VALUES(`Valuation Class`),
            `Created by` = VALUES(`Created by`),
            `Last change` = VALUES(`Last change`),
            `Price` = VALUES(`Price`);
        """
        cursor.execute(query, (material, material_description, text_chars, base_unit_of_measure, 
                            material_group, material_type, plant, df_at_client_level, 
                            valuation_class, created_by, last_change, price))
        self.connection.commit()
        cursor.close()

    def close(self):
            """Close the database connection."""
            self.connection.close()


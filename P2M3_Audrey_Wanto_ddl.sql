CREATE TABLE table_m3 (
	"Rank" INT,
	"Name" VARCHAR(500),
	"Platform" VARCHAR(500),
	"Year" VARCHAR(500),
	"Genre" VARCHAR(500),
	"Publisher" VARCHAR(500),
	"NA_Sales" FLOAT,
	"EU_Sales" FLOAT,
	"JP_Sales" FLOAT,
	"Other_Sales" FLOAT,
	"Global_Sales" FLOAT
)

COPY table_m3("Rank", "Name", "Platform", "Year", "Genre", "Publisher", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales")
FROM 'C:\Users\wanto\OneDrive\Desktop\Hacktiv8\Phase_2\M3\P2M3_Audrey_Wanto_data_raw.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM table_m3
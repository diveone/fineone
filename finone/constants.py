from finone import app

#: Auth credentials
AUTH_LICENSEKEY = app.config['MORTECH_LICENSEKEY']
AUTH_NAME = app.config['MORTECH_THIRDPARTY_NAME']
AUTH_ID = app.config['MORTECH_CUSTOMER_ID']
AUTH_EMAIL = app.config['MORTECH_EMAIL']


#: Service request parameters
class ServiceConstants:
    LICENSEKEY = 'licenseKey'
    THIRD_PARTY_NAME = 'thirdPartyName'
    CUSTOMER_ID = 'customerId'
    EMAIL_ADDRESS = 'emailAddress'
    REQUEST_ID = 'request_id'
    PROPERTY_STATE = 'propertyState'
    PROPERTY_COUNTY = 'propertyCounty'
    LOAN_AMOUNT = 'loan_amount'
    PROPERTY_TYPE = 'propertyType'
    LOAN_PURPOSE = 'loanpurpose'
    APPRAISED_VALUE = 'appraisedvalue'
    TARGET_PRICE = 'targetPrice'
    LOCKIN_DAYS = 'lockindays'
    LOAN_PRODUCT1 = 'loanProduct1'
    LOAN_PRODUCT2 = 'loanProduct2'
    LOAN_PRODUCT3 = 'loanProduct3'
    LOAN_PRODUCT4 = 'loanProduct4'
    LOAN_PRODUCT5 = 'loanProduct5'


#: Service request default values
DEFAULT_LOCKIN = '45'
DEFAULT_TARGET_PRICE = '-999'

PRODUCT_FIXED = 'Fixed'
PRODUCT_ARM = 'Variable'

PRODUCT_30_FIXED = '30 year fixed'
PRODUCT_15_FIXED = '15 year fixed'
PRODUCT_5_ARM = '5 year ARM/30 yrs'
PRODUCT_7_ARM = '7 year ARM/30 yrs'

#: Loan purpose values for service requests
LOAN_PURPOSE_PURCHASE = 0
LOAN_PURPOSE_RATE_AND_TERM = 1  # Refi
LOAN_PURPOSE_CASHOUT = 2        # Refi
LOAN_PURPOSE_HOME_EQUITY = 3    # Refi
LOAN_PURPOSE_HELOC = 4          # Refi

#: Loan purpose types
PURCHASE = 'purchase'
REFINANCE = 'refinance'
CASHOUT = 'cashout'
HOME_EQUITY = 'home_equity'
HELOC = 'heloc'

#: Map of loan purpose types to loan purpose service values
LOAN_PURPOSE_MAP = {
	PURCHASE: LOAN_PURPOSE_PURCHASE,
	REFINANCE: LOAN_PURPOSE_RATE_AND_TERM,
	CASHOUT: LOAN_PURPOSE_CASHOUT,
	HOME_EQUITY: LOAN_PURPOSE_HOME_EQUITY,
	HELOC: LOAN_PURPOSE_HELOC
}

#: Property type values for service requests
PROPERTY_TYPE_ATTACHED = 0
PROPERTY_TYPE_DETACHED = 1
PROPERTY_TYPE_COOPS = 2
PROPERTY_TYPE_CONDOS_LIMITED = 3
PROPERTY_TYPE_CONDOS_LOW = 4   # 1-4
PROPERTY_TYPE_CONDOS_MID = 5   # 5-8
PROPERTY_TYPE_CONDOS_HIGH = 6  # >8
PROPERTY_TYPE_CONDOS_UNAPPROVED = 7
PROPERTY_TYPE_CONDOTELS = 8
PROPERTY_TYPE_LEASEHOLD = 9
PROPERTY_TYPE_LOG_HOMES = 10
PROPERTY_TYPE_MANUFACTURED_HOME = 11
PROPERTY_TYPE_MIXED_USE = 12
PROPERTY_TYPE_MODEL_HOMES = 13
PROPERTY_TYPE_MODULAR = 14
PROPERTY_TYPE_LISTED_FOR_SALE = 15
PROPERTY_TYPE_PUDS = 16
PROPERTY_TYPE_PUDS_UNAPPROVED = 17
PROPERTY_TYPE_RURAL = 18
PROPERTY_TYPE_TOWNHOMES = 19
PROPERTY_TYPE_2_UNIT = 20
PROPERTY_TYPE_3_UNIT = 21
PROPERTY_TYPE_4_UNIT = 22
PROPERTY_TYPE_MAP = {
    'single_family': PROPERTY_TYPE_ATTACHED,
    'condo_low': PROPERTY_TYPE_CONDOS_LOW,
    'condo_med': PROPERTY_TYPE_CONDOS_MID,
    'condo_high': PROPERTY_TYPE_CONDOS_HIGH,
    # TODO: Verify PUD_HAS_HOA == PUDS
    'puds': PROPERTY_TYPE_PUDS,
    'townhouse': PROPERTY_TYPE_TOWNHOMES,
    '2_unit': PROPERTY_TYPE_2_UNIT,
    '3_unit': PROPERTY_TYPE_3_UNIT,
    '4_unit': PROPERTY_TYPE_4_UNIT,
    # TODO: Mortech has no vacant lot option. Change to rural?
    'rural': PROPERTY_TYPE_RURAL,
    'manufactured': PROPERTY_TYPE_MANUFACTURED_HOME
}

OCCUPANCY_TYPE_OWNER_OCCUPIED = 0
OCCUPANCY_TYPE_NON_OWNER_OCCUPIED = 1
OCCUPANCY_TYPE_SECOND_HOME = 2
OCCUPANCY_MAP = {
	'primary_home': OCCUPANCY_TYPE_OWNER_OCCUPIED,
	'secondary_home': OCCUPANCY_TYPE_SECOND_HOME,
	'investment': OCCUPANCY_TYPE_NON_OWNER_OCCUPIED
}

# TODO: XML Elements & @Attributes
quote = 'quote'
vendor_name = '@vendor_name'
product_desc = '@productDesc'
product_term = '@productTerm'
initial_arm = '@initialArmTerm'
int_only_months = '@intOnlyMonths'
quote_detail = 'quote_detail'
rate = '@rate'
price = '@price'
origination_fee = '@originationFee'

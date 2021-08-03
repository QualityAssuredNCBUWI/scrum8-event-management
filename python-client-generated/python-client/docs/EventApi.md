# swagger_client.EventApi

All URIs are relative to *https://petstore.swagger.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_event**](EventApi.md#add_event) | **POST** /event | Add a new event
[**api_event_event_id_put**](EventApi.md#api_event_event_id_put) | **PUT** /api/event/{eventId} | Edit event by ID
[**getevent_by_id**](EventApi.md#getevent_by_id) | **GET** /api/event/{eventId} | Find event by ID
[**remove_event**](EventApi.md#remove_event) | **DELETE** /api/event/{eventId} | Delete event
[**update_pet**](EventApi.md#update_pet) | **PUT** /event | Update an existing pet


# **add_event**
> add_event(body)

Add a new event



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventApi()
body = swagger_client.Event() # Event | Parameters needed for the creation of a new Event object

try:
    # Add a new event
    api_instance.add_event(body)
except ApiException as e:
    print("Exception when calling EventApi->add_event: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Event**](Event.md)| Parameters needed for the creation of a new Event object | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/xml, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_event_event_id_put**
> Event api_event_event_id_put(event_id)

Edit event by ID

make and edit to a single Event based on ID number

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: JWT_Token
configuration = swagger_client.Configuration()
configuration.api_key['JWT_token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWT_token'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.EventApi(swagger_client.ApiClient(configuration))
event_id = 56 # int | 

try:
    # Edit event by ID
    api_response = api_instance.api_event_event_id_put(event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->api_event_event_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event_id** | **int**|  | 

### Return type

[**Event**](Event.md)

### Authorization

[JWT_Token](../README.md#JWT_Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getevent_by_id**
> Event getevent_by_id(event_id)

Find event by ID

Returns a single pet

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['api_key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.EventApi(swagger_client.ApiClient(configuration))
event_id = 789 # int | ID of event to return

try:
    # Find event by ID
    api_response = api_instance.getevent_by_id(event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->getevent_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event_id** | **int**| ID of event to return | 

### Return type

[**Event**](Event.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/xml, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_event**
> Event remove_event(event_id)

Delete event

Delete event by Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: JWT_Token
configuration = swagger_client.Configuration()
configuration.api_key['JWT_token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['JWT_token'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.EventApi(swagger_client.ApiClient(configuration))
event_id = 789 # int | 

try:
    # Delete event
    api_response = api_instance.remove_event(event_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EventApi->remove_event: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event_id** | **int**|  | 

### Return type

[**Event**](Event.md)

### Authorization

[JWT_Token](../README.md#JWT_Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_pet**
> update_pet(body)

Update an existing pet



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EventApi()
body = swagger_client.Pet() # Pet | Pet object that needs to be added to the store

try:
    # Update an existing pet
    api_instance.update_pet(body)
except ApiException as e:
    print("Exception when calling EventApi->update_pet: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Pet**](Pet.md)| Pet object that needs to be added to the store | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/xml
 - **Accept**: application/xml, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


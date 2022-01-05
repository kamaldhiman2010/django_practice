from django.http import HttpResponse

# def my_middleware(get_response):
#     print("one time Initializtion")
#     def my_function(request):
#         print("this is before view")
#         response=get_response(request)
#         print("this is after view")
#         return response
#     return my_function
#
# class my_middleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#         print("one time initilization")
#
#     def __call__(self,request):
#         print("this is before view")
#         response=self.get_response(request)
#         print("after view")
#         return response



class MyProcessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(request, *args, **kwargs):
        print("process view")
        # return HttpResponse("this is before view")
        return None


# class MyExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_exception(self, request, exception):
#         print("exception occured")
#         class_name = exception.__class__.__name__
#         print(class_name)
#         msg = exception
#         return HttpResponse(msg)


class MyTemplateResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        print("Process Templates Response from middleware")
        response.context_data['name'] = 'Sonam'
        print("template data")
        return response

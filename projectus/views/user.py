from django.shortcuts import render

def login(request):
    return render(
        request,
        'projectus/home.html'
    )


def logout(request):
    return render(
        request,
        'projectus/home.html'
    )

def profile(request):
    return render(
        request,
        'projectus/home.html'
    )

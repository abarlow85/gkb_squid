from django.conf.urls import url
import views


urlpatterns = [
	
	url(r'^$', views.home),
	url(r'^form/$', views.form_data),
    url(r'^create_category/$', views.create_category),
    url(r'^inventory/$', views.get_inv),
    url(r'^componentForm/$', views.component_data)
    url(r'^samplePost/$', views.sample_post),
    url(r'^print/$', views.print_label),
]
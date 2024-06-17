from django import forms
from django.utils.safestring import mark_safe

class Select2Widget(forms.TextInput):
    template_name = 'patients/select2.html'

    def __init__(self, url, queryParam, *args, **kwargs):
        self.url = url
        self.queryParam = queryParam
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['url'] = self.url
        context['queryParam'] = self.queryParam
        return context

    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(self.attrs, attrs)
        html = super().render(name, value, attrs)
        js = f"""
        <script type="text/javascript">
            $(document).ready(function() {{
                $('#id_{name}').select2({{
                    ajax: {{
                        url: '{self.url}',
                        dataType: 'json',
                        delay: 250,
                        data: function (params) {{
                            return {{
                                {self.queryParam}: (params.term + '00').substring(0, 5)
                            }};
                        }},
                        processResults: function (data) {{
                            return {{
                                results: $.map(data, function(item) {{
                                    return {{
                                        id: item.nom,
                                        text: item.nom
                                    }}
                                }})
                            }};
                        }},
                        cache: true
                    }},
                    minimumInputLength: 3,
                }});
            }});
        </script>
        """
        return mark_safe(html + js)
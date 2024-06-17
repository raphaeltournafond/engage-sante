from django import forms
from django.utils.safestring import mark_safe

class Select2Widget(forms.TextInput):
    template_name = 'patients/select2.html'

    def __init__(self, url, queryParam, placeholder = '', fillWith = '', minLength = 3, maxLength = 5,  *args, **kwargs):
        self.url = url
        self.queryParam = queryParam
        self.placeholder = placeholder
        self.fillWith = fillWith
        self.minLength = minLength
        self.maxLength = maxLength
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['url'] = self.url
        context['queryParam'] = self.queryParam
        context['placeholder'] = self.placeholder
        context['fillWith'] = self.fillWith
        context['minLength'] = self.minLength
        context['maxLength'] = self.maxLength
        return context

    def render(self, name, value, attrs=None, renderer=None):
        attrs = self.build_attrs(self.attrs, attrs)
        html = super().render(name, value, attrs)
        js = f"""
        <script type="text/javascript">
            $(document).ready(function() {{
                if ('{value}') {{
                    var option = new Option('{value}', '{value}', true, true);
                    $('#id_{name}').append(option).trigger('change');
                }}
                $('#id_{name}').select2({{
                    ajax: {{
                        url: '{self.url}',
                        dataType: 'json',
                        delay: 250,
                        data: function (params) {{
                            return {{
                                {self.queryParam}: (params.term + `{self.fillWith}`).substring(0, {self.maxLength})
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
                    minimumInputLength: {self.minLength},
                    placeholder: `{self.placeholder}`,
                }});
            }});
        </script>
        """
        return mark_safe(html + js)
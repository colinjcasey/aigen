import os
import args_manager
import modules.config

from PIL import Image
from modules.util import generate_temp_filename


log_cache = {}


def get_current_html_path():
    date_string, local_temp_filename, only_name = generate_temp_filename(folder=modules.config.path_outputs,
                                                                         extension='png')
    html_name = os.path.join(os.path.dirname(local_temp_filename), 'log.html')
    return html_name


def log(img, dic):
    if args_manager.args.disable_image_log:
        return

    date_string, local_temp_filename, only_name = generate_temp_filename(folder=modules.config.path_outputs, extension='png')
    os.makedirs(os.path.dirname(local_temp_filename), exist_ok=True)
    Image.fromarray(img).save(local_temp_filename)
    html_name = os.path.join(os.path.dirname(local_temp_filename), 'log.html')

    css_styles = (
        "<style>"
        "body { background-color: #121212; color: #E0E0E0; } "
        "a { color: #BB86FC; } "
        ".metadata { border-collapse: collapse; width: 100%; } "
        ".metadata .key { width: 15%; } "
        ".metadata .value { width: 85%; font-weight: bold; } "
        ".metadata th, .metadata td { border: 1px solid #4d4d4d; padding: 4px; } "
        ".image-container img { height: auto; max-width: 512px; display: block; padding-right:10px; } "
        ".image-container div { text-align: center; padding: 4px; } "
        "hr { border-color: gray; } "
        "</style>"
    )

    begin_part = f"<html><head><title>Fooocus Log {date_string}</title>{css_styles}</head><body><p>Fooocus Log {date_string} (private)</p>\n<p>All images are clean, without any hidden data/meta, and safe to share with others.</p><!--fooocus-log-split-->\n\n"
    end_part = f'\n<!--fooocus-log-split--></body></html>'

    middle_part = log_cache.get(html_name, "")

    if middle_part == "":
        if os.path.exists(html_name):
            existing_split = open(html_name, 'r', encoding='utf-8').read().split('<!--fooocus-log-split-->')
            if len(existing_split) == 3:
                middle_part = existing_split[1]
            else:
                middle_part = existing_split[0]

    div_name = only_name.replace('.', '_')
    item = f"<div id=\"{div_name}\" class=\"image-container\"><hr><table><tr>\n"
    item += f"<td><a href=\"{only_name}\" target=\"_blank\"><img src='{only_name}' onerror=\"this.closest('.image-container').style.display='none';\" loading='lazy'></img></a><div>{only_name}</div></td>"
    item += "<td><table class='metadata'>"
    for key, value in dic:
        item += f"<tr><td class='key'>{key}</td><td class='value'>{value}</td></tr>\n"
    item += "</table>"
    item += "</td>"
    item += "</tr></table></div>\n\n"

    middle_part = item + middle_part

    with open(html_name, 'w', encoding='utf-8') as f:
        f.write(begin_part + middle_part + end_part)

    print(f'Image generated with private log at: {html_name}')

    log_cache[html_name] = middle_part

    return

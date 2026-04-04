require 'nokogiri'

Jekyll::Hooks.register [:pages, :posts], :post_render do |doc, payload|
  doc.output = wrap_table_with_div(doc.output) if doc.output
end

def wrap_table_with_div(html)
  return html unless html

  doc = Nokogiri::HTML.fragment(html)

  doc.css('table').each do |table|
    # 添加 table 样式 class
    existing_class = table['class']
    if existing_class
      table['class'] = "table table-bordered table-light table-striped table-hover #{existing_class}"
    else
      table['class'] = "table table-bordered table-light table-striped table-hover"
    end

    # 创建 wrapper div
    wrapper = Nokogiri::XML::Node.new('div', doc)
    wrapper['class'] = 'table-responsive'

    # 将 table 用 wrapper 包裹
    table.replace(wrapper)
    wrapper.add_child(table)
  end

  doc.to_html
end

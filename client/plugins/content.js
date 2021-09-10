function getValue(element) {
  return element.value ? element.value : element.children[0].value
}

export default ({ $content }, inject) => {
  inject('getContent', async name => {
    const content = await $content(name).fetch()

    const data = []
    for (const element of content.body.children) {
      if (element.tag === 'h1' || element.tag === 'h2') {
        data.push({
          name: getValue(element.children[0]),
          description: '',
        })
      } else if (element.tag === 'p') {
        data[data.length - 1].description += getValue(element.children[0]).replace(/\n/g, ' ')
      } else if (element.tag === 'ul') {
        for (const element2 of element.children) {
          if (element2.tag === 'li') {
            const value = element2.children.map(element3 => getValue(element3)).join('')
            const key = value.split(': ')[0].toLowerCase()
            data[data.length - 1][key] = value.split(': ').slice(1).join(': ')
          }
        }
      } else if (element.type === 'text' && element.value === '\n') {
        data[data.length - 1].description += '\n\n'
      }
    }

    for (const [index] of data.entries()) {
      data[index].description = data[index].description.trim()
    }

    return data
  })
}

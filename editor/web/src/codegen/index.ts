import ejs from 'ejs';

import jsTemplate from './js.ejs?raw';
import jsonTemplate from './json.ejs?raw';
import pythonTemplate from './python.ejs?raw';

interface CodeGen {
  name: string;
  language: string;
  generate(params: any): string;
}

class EjsCodeGen implements CodeGen {
  name: string;
  language: string;
  private template: ejs.TemplateFunction;
  constructor(name: string, language: string, templateContent: any) {
    this.name = name;
    this.language = language;
    this.template = ejs.compile(templateContent);
  }
  generate(params: any): string {
    return this.template({ params });
  }
}

export const jsCodeGen = new EjsCodeGen('NodeJS Example', 'javascript', jsTemplate);
export const jsonCodeGen = new EjsCodeGen('JSON', 'json', jsonTemplate);
export const pythonCodeGen = new EjsCodeGen('Python Example', 'python', pythonTemplate);

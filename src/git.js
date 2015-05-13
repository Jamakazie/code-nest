'use strict';

import polyfill from 'babel/polyfill';
import util from 'util';
import fs from 'fs';
import path from 'path';
import Promise from 'bluebird';

var mkdirAsync = Promise.promisify(fs.mkdir);

import { exec } from 'child_process';
var execAsync = Promise.promisify(exec);

import { get } from 'needle';
var getAsync = Promise.promisify(get);


import { Repo } from './models.js';

export var clone = Promise.coroutine(function* (gulp_cb) {
  let repos = yield Repo.find().exec();
  if (!repos.length) {
    console.log('No repos found in mongodb, exiting');
    return;
  }

  let repo_dir = path.join(path.dirname(__dirname), 'repos');
  try {
    yield mkdirAsync(repo_dir, 484);
  } catch (e) {
    console.log(e);
  }

  //repos.length
  for (let i = 0; i < repos.length; i++) {
    let repo = repos[i];
    try {
      console.log(`Cloning ${repo.git_url} ...`);
      let out = yield execAsync(`git clone ${repo.git_url}`, { cwd: repo_dir });
      console.log(out[1]);
    } catch (e) {
      console.log(e);
    }
  }

  if (typeof gulp_cb === 'undefined') return;
  return gulp_cb();
});
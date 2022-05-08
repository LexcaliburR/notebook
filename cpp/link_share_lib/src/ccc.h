/*
 * @Author: lishiqi lishiqi@lishiqi.con
 * @Date: 2022-05-09 01:33:20
 * @LastEditors: lishiqi lishiqi@lishiqi.con
 * @LastEditTime: 2022-05-09 02:09:52
 * @FilePath: /cpp/动态库连接是否会传递/src/aaa copy 2.h
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
#pragma once

class C
{
public:
    C();
    C(const C &c) = delete;
    ~C();
};
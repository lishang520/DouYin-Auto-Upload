# -*- coding: utf-8 -*-
from playwright.async_api import Playwright, async_playwright
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os,sys
import asyncio
import shutil

def set_env():
    # 如果目录source_videos不存在则创建  用于存放待上传的视频
    # 如果目录source_videos不存在则创建  用于初始的视频
    if not os.path.exists('/source_videos'):
        os.mkdir('/source_videos')
        print("[+] 请在'source_videos'目录下放入视频")
    if not os.path.exists('cookie.json') :
        print('[+] cookie文件不存在，即将自动打开浏览器，请扫码登录，登陆后会自动生成cookie文件')
        os.system('python3 -m playwright install')  # 生成cookie文件
        os.system('playwright codegen www.douyin.com --save-storage=cookie.json')   #生成cookie文件

class set_video(object):
    def __init__(self):
        self.text = ''  # 视频标题
        self.path = './'   # 脚本运行目录
        self.path_wait =''
        self.path_source = ''
        self.get_filenames()

    def get_filenames(self):
        #如果wait_upload目录不存在则创建  用于存放待上传的视频
        self.path_wait = self.path + 'wait_upload/'
        if not os.path.exists(self.path_wait):
            os.mkdir(self.path_wait)
        #清空目录下的所有文件 防止重复上传
        for root, dirs, files in os.walk(self.path_wait):
            for name in files:
                os.remove(os.path.join(root, name))
        #将source_videos目录下的视频随机移动1个到wait_upload目录下,并获取它的文件名，将其赋值给self.text
        self.path_source = self.path + 'source_videos/'  # 视频源目录 用于存放待上传的视频  请将视频放到此目录下
        files = os.listdir(self.path_source)
        if len(files) < 1 :
            print('[！Warning！]视频源目录下没有视频')
            sys.exit()
        shutil.move(self.path_source + files[0], self.path_wait  + files[0])
        self.text = files[0].split('.')[0]

def title():
    print('''\033[34m                                                                                                                                                                                                                                                   
                                            iiii                             tttt                                                  
                                           i::::i                         ttt:::t                                                  
                                            iiii                          t:::::t                                                  
                                                                          t:::::t                                                  
    ppppp   ppppppppp     aaaaaaaaaaaaa   iiiiiii nnnn  nnnnnnnn    ttttttt:::::ttttttt        eeeeeeeeeeee    rrrrr   rrrrrrrrr   
    p:::::::::::::::::p   aaaaaaaaa:::::a  i::::i n::::::::::::::nn t:::::::::::::::::t     e::::::eeeee:::::eer:::::::::::::::::r 
    pp::::::ppppp::::::p           a::::a  i::::i nn:::::::::::::::ntttttt:::::::tttttt    e::::::e     e:::::err::::::rrrrr::::::r
     p:::::p     p:::::p    aaaaaaa:::::a  i::::i   n:::::nnnn:::::n      t:::::t          e:::::::eeeee::::::e r:::::r     r:::::r
     p:::::p     p:::::p  aa::::::::::::a  i::::i   n::::n    n::::n      t:::::t          e:::::::::::::::::e  r:::::r     rrrrrrr
     p:::::p     p:::::p a::::aaaa::::::a  i::::i   n::::n    n::::n      t:::::t          e::::::eeeeeeeeeee   r:::::r            
     p:::::p    p::::::pa::::a    a:::::a  i::::i   n::::n    n::::n      t:::::t    tttttte:::::::e            r:::::r            
     p:::::ppppp:::::::pa::::a    a:::::a i::::::i  n::::n    n::::n      t::::::tttt:::::te::::::::e           r:::::r            
     p::::::::::::::::p a:::::aaaa::::::a i::::::i  n::::n    n::::n      tt::::::::::::::t e::::::::eeeeeeee   r:::::r                  
     p::::::pppppppp      aaaaaaaaaa  aaaaiiiiiiii  nnnnnn    nnnnnn          ttttttttttt      eeeeeeeeeeeeee   rrrrrrr            
     p:::::p                                                                                                                                                                                                                                            
    p:::::::p                                                                                                                      
    p:::::::p                                                                                                                
    p:::::::p                                    What is black and what is white                                                                              
    ppppppppp                                    blog： https://www.cnblogs.com/painter-sec  
                                                 Github： https://github.com/lishang520                                                                                                                                                                                                                                             
    \033[0m''')


class pw(set_video):
    def __init__(self):
        super(pw, self).__init__()

    async def upload(self, playwright: Playwright) -> None:
        # 使用 Chromium 浏览器启动一个浏览器实例
        browser = await playwright.chromium.launch(headless=False)
        # 创建一个浏览器上下文，使用指定的 cookie 文件
        context = await browser.new_context(storage_state=self.path + "\\cookie.json")

        # 创建一个新的页面
        page = await context.new_page()
        # 访问指定的 URL
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        print('[+]正在上传-------{}.mp4'.format(self.text))
        # 等待页面跳转到指定的 URL，没进入，则自动等待到超时
        print('  [-]正在打开主页...')
        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload")
        # 点击 "上传视频" 按钮
        await page.locator("label:has-text(\"为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").set_input_files("{}.mp4".format(self.path_wait + self.text))
        # # 点击我知道了
        # while True:
        #     #判断是否弹出来“我知道了”这个弹窗
        #     try:
        #         await page.locator('//*[@id="dialog-0"]/div/div/div/div[3]').click()
        #         break
        #     except:
        #         print("[-] 正在检测“我知道了”这个弹窗")
        #         time.sleep(0.1)

        # 等待页面跳转到指定的 URL
        while True:
            #判断是是否进入视频发布页面，没进入，则自动等待到超时
            try:
                await page.wait_for_url("https://creator.douyin.com/creator-micro/content/publish")
                break
            except:
                print("  [-] 正在等待进入视频发布页面...")
                time.sleep(0.1)
        # 填充标题和话题
        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(self.text + '#生活不会辜负每一个努力的人 #只有经历过的人才会懂 #一定要看到最后 ')           #视频标题
        # 判断是否上传完毕
        while True:
            #判断重新上传按钮是否存在，如果不存在，代表视频正在上传，则等待
            try:
                #匹配到重新上传按钮，代表视频上传完毕
                number = await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div').count()
                if number > 0:
                    print("  [-]视频上传完毕")
                    break
                else:
                    print("  [-] 正在上传视频中...")
                    time.sleep(2)
            except:
                print("  [-] 正在上传视频中...")
                time.sleep(2)

        #判断视频是否发布成功
        while True:
            #判断视频是否发布成功

            try:
                await page.locator(
                    'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()  # 点击 "发布" 按钮
                await page.wait_for_url("https://creator.douyin.com/creator-micro/content/manage",timeout=1500)   #如果自动跳转到作品页面，则代表发布成功
                print("  [-]视频发布成功")
                break
            except:
                print("  [-] 视频正在发布中...")
                time.sleep(0.5)

        await context.storage_state(path=self.path + "\\cookie.json")   #保存cookie
        print('  [-]cookie更新完毕！')
        time.sleep(2)   #这里延迟是为了方便眼睛直观的观看
        # 关闭浏览器上下文和浏览器实例
        await context.close()
        await browser.close()
        print('[+]正在监控执行计划中.......')

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)


def job_1():
    app = pw()
    asyncio.run(app.main())

if __name__ == '__main__':
    title()
    set_env()  #初始化环境
    job_detail = ''    #定时上传详情
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    mes_input = input('''
    [-]请输入你要自动上传的时间点，请在英文状态下输入，用逗号分割,可以多个时间，例如：  
        13:36,13:39,13:42     #表示每天的13点36分，13点39分，13点42分自动上传作品
    ''')
    upload_time = mes_input.replace('，',',').replace('：',':').split(',')    #替换，防止用户输入中文逗号和冒号
    # upload_time = ['13:36','13:39','13:42']   #每天的发布作品的时间，用冒号分割
    for t in upload_time:
        h,m = t.split(':')
        scheduler.add_job(job_1, 'cron', day='1-31', hour=h, minute=m, misfire_grace_time=180)
        job_detail += '  \033[1;32m[-]每天{}点{}分发布作品\033[0m\n'.format(h,m)
    print('\033[1;31m-------作品定时自动上传已经启动，请不要关闭本窗口，上传计划如下：-------\033[0m')   #这2个打印的必须要放在scheduler.start()前面，否则不会打印
    print(job_detail)   #这2个打印的必须要放在scheduler.start()前面，否则不会打印
    scheduler.start()



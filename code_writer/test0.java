// Java后端框架示例代码

import .util.List;
import .util.ArrayList;

// 实体类，对应数据表user
class User {
    private int id;
    private String name;
    private int age;

    public User(int id, String name, int age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }

    // getter和setter方法省略
}

// DAO（数据访问对象）层，负责数据库相关操作
class UserDao {
    // 模拟数据库中的数据存储
    private static List<User> userList = new ArrayList<>();

    static {
        User user1 = new User(1, "张三", 20);
        User user2 = new User(2, "李四", 25);
        userList.add(user1);
        userList.add(user2);
    }

    // 获取所有用户信息
    public List<User> getAllUsers() {
        return userList;
    }

    // 根据id获取用户信息
    public User getUserById(int id) {
        for (User user : userList) {
            if (user.getId() == id) {
                return user;
            }
        }
        return null;
    }

    // 新增用户
    public void addUser(User user) {
        userList.add(user);
    }

    // 更新用户信息
    public void updateUser(User newUser) {
        for (User user : userList) {
            if (user.getId() == newUser.getId()) {
                user.setName(newUser.getName());
                user.setAge(newUser.getAge());
                break;
            }
        }
    }

    // 删除用户信息
    public void deleteUser(int id) {
        for (User user : userList) {
            if (user.getId() == id) {
                userList.remove(user);
                break;
            }
        }
    }
}

// 服务层，负责处理业务逻辑
class UserService {
    private UserDao userDao = new UserDao();

    // 获取所有用户信息
    public List<User> getAllUsers() {
        return userDao.getAllUsers();
    }

    // 根据id获取用户信息
    public User getUserById(int id) {
        return userDao.getUserById(id);
    }

    // 新增用户
    public void addUser(User user) {
        userDao.addUser(user);
    }

    // 更新用户信息
    public void updateUser(User newUser) {
        userDao.updateUser(newUser);
    }

    // 删除用户信息
    public void deleteUser(int id) {
        userDao.deleteUser(id);
    }
}

// 控制器，负责处理请求和响应
class UserController {
    private UserService userService = new UserService();

    // 获取所有用户信息
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }

    // 根据id获取用户信息
    public User getUserById(int id) {
        return userService.getUserById(id);
    }

    // 新增用户
    public void addUser(User user) {
        userService.addUser(user);
    }

    // 更新用户信息
    public void updateUser(User newUser) {
        userService.updateUser(newUser);
    }

    // 删除用户信息
    public void deleteUser(int id) {
        userService.deleteUser(id);
    }
}

// 入口类
public class Main {
    public static void main(String[] args) {
        UserController userController = new UserController();

        // 新增用户
        User user3 = new User(3, "王五", 30);
        userController.addUser(user3);

        // 获取所有用户信息
        List<User> userList = userController.getAllUsers();
        for (User user : userList) {
            System.out.println(user.getId() + ": " + user.getName() + ", " + user.getAge());
        }

        // 更新用户信息
        User user2 = userController.getUserById(2);
        user2.setName("新李四");
        userController.updateUser(user2);

        // 删除用户信息
        userController.deleteUser(1);
    }
}